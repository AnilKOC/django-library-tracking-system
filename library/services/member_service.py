from typing import Optional

from core.services.base_service import BaseService
from library.models import Member
from library.repositories.loan_repository import LoanRepository
from library.repositories.member_repository import MemberRepository


class MemberService(BaseService[Member]):
    def __init__(
        self,
        repo: Optional[MemberRepository] = None,
    ):
        super().__init__(repo or MemberRepository())
        self.loan_repo = LoanRepository()

    def get_top_active_memebers(self):
        from django.db.models import Count, Q

        from library.models import Loan, Member

        active_members = Loan.models.aggregate(
            active_loans=Count("members"),
        )
