from datetime import timedelta
from typing import Optional

from django.utils import timezone

from core.services.base_service import BaseService
from library.exceptions import LoanOverdueException
from library.models import Loan
from library.repositories.loan_repository import LoanRepository


class LoanService(BaseService[Loan]):
    def __init__(
        self,
        repo: Optional[LoanRepository] = None,
    ):
        super().__init__(repo or LoanRepository())

    def get_overdue_loans(self):
        return self.repo.get_overdue_loans()

    def extend_loan_additional_days(self, loan_id: int, additional_days: int) -> Loan:
        loan = self.repo.get_by_id(pk=loan_id)
        if loan.due_date < timezone.now():
            return LoanOverdueException("Loan is already overdued.")
        loan.due_date = loan.due_date + timedelta(days=additional_days)
        loan.save()

        return loan
