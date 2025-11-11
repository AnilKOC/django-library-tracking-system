from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.timezone import datetime

from core.utils.task_lock import task_lock
from library.services.loan_service import LoanService

from .models import Loan


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def send_overdue_loan_notification():
    service = LoanService()
    loans = service.get_overdue_loans()

    for loan in loans.iterator(chunk_size=25):  # This is for optimized task workflow.
        days_overdue = (datetime.today() - loan.return_date).days
        if not cache.set(
            f"overdue_mails:{loan.member.user.email}", "", timeout=60 * 60 * 24
        ):  # This is for idempotency.
            send_mail(
                subject=f"Overdue Notice: {loan.book.title}",
                message=(
                    f"Dear {loan.member.user.first_name},\n\n"
                    f'Our records show that your loan for "{loan.book.title}" '
                    f"is {days_overdue} day{'s' if days_overdue > 1 else ''} overdue.\n"
                    f"Please return the book to the library as soon as possible "
                    f"to avoid additional late fees.\n\n"
                    f"Thank you for your prompt attention.\n\n"
                    f"— Library Management System"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
