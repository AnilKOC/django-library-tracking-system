from datetime import date
from typing import Optional

from django.db import transaction
from django.utils import timezone
from tasks import send_loan_notification

from core.services.base_service import BaseService
from library.models import Book, Loan, Member
from library.repositories.book_repository import BookRepository
from library.repositories.loan_repository import LoanRepository


class BookService(BaseService[Book]):
    def __init__(
        self,
        repo: Optional[BookRepository] = None,
        loan_repo: Optional[LoanRepository] = None,
    ):
        super().__init__(repo or BookRepository())
        self.loan_repo = loan_repo or LoanRepository()

    @transaction.atomic
    def loan_book(self, book_id: int, member_id: int) -> dict:
        book = self.repo.get_by_id(book_id)
        if not book:
            return {"error": "Book does not exist."}

        if book.available_copies < 1:
            return {"error": "No available copies."}

        member = Member.objects.filter(id=member_id).first()
        if not member:
            return {"error": "Member does not exist."}

        loan = self.loan_repo.create(book=book, member=member)
        book.available_copies -= 1
        book.save()

        send_loan_notification.delay(loan.id)

        return {"status": "Book loaned successfully.", "loan_id": loan.id}

    @transaction.atomic
    def return_book(self, book_id: int, member_id: int) -> dict:
        book = self.repo.get_by_id(book_id)
        if not book:
            return {"error": "Book does not exist."}

        loan = Loan.objects.filter(
            book=book, member__id=member_id, is_returned=False
        ).first()
        if not loan:
            return {"error": "Active loan does not exist."}

        loan.is_returned = True
        loan.return_date = timezone.now().date()
        loan.save()

        book.available_copies += 1
        book.save()

        return {"status": "Book returned successfully."}
