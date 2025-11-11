from datetime import date

from django.db.models import Q

from core.repositories.base_repository import BaseRepository
from library.models import Loan


class LoanRepository(BaseRepository[Loan]):
    def __init__(self):
        super().__init__(Loan)

    def find_active_loans(self):
        return self.filter(is_returned=False)

    def find_loans_by_member(self, member_id: int):
        return self.filter(member_id=member_id)

    def find_overdue_loans(self):
        return self.filter(is_returned=False, return_date__lt=date.today())

    def search_loans(self, keyword: str):
        return self.search(
            Q(book__title__icontains=keyword)
            | Q(member__user__username__icontains=keyword)
        )

    def get_overdue_loans(self):
        return self.filter(due_date__lte=date.today(), is_returned=False)
