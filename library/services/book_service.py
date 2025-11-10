from datetime import date
from typing import Optional

from django.db import transaction
from django.utils import timezone
from tasks import send_loan_notification

from core.services.base_service import BaseService
from library.exceptions import (ActiveLoanNotFound, BookNotFound,
                                MemberNotFound, NoAvailableCopies)
from library.repositories.book_repository import BookRepository
from library.repositories.loan_repository import LoanRepository
from library.repositories.member_repository import MemberRepository


class BookService(BaseService[Book]):
    def __init__(
        self,
        repo: Optional[BookRepository] = None,
        loan_repo: Optional[LoanRepository] = None,
        member_repo: Optional[MemberRepository] = None,
    ):
        super().__init__(repo or BookRepository())
        self.loan_repo = loan_repo or LoanRepository()
        self.member_repo = member_repo or MemberRepository()

    @transaction.atomic
    def loan_book(self, book_id: int, member_id: int) -> dict:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise BookNotFound("Book does not exist.")

        if book.available_copies < 1:
            raise NoAvailableCopies("No available copies.")

        member = self.member_repo.get_by_id(pk=member_id)
        if not member:
            raise MemberNotFound("Member does not exist.")

        loan = self.loan_repo.create(book=book, member=member)
        book.available_copies -= 1
        book.save()

        send_loan_notification.delay(loan.id)

        return loan

    @transaction.atomic
    def return_book(self, book_id: int, member_id: int) -> dict:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise BookNotFound("Book does not exist.")

        loan = self.loan_repo.filter(
            book=book, member__id=member_id, is_returned=False
        ).first()
        if not loan:
            raise ActiveLoanNotFound("Active loan does not exist.")

        loan.is_returned = True
        loan.return_date = timezone.now().date()
        loan.save()

        book.available_copies += 1
        book.save()

        return loan
