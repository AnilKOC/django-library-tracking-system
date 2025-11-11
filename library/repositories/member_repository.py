from typing import Iterable

from django.contrib.auth.models import User
from django.db.models import Q

from core.repositories.base_repository import BaseRepository, T
from library.models import Member


class MemberRepository(BaseRepository[Member]):
    def __init__(self):
        super().__init__(Member)

    def find_by_username(self, username: str):
        return self.search(Q(user__username__icontains=username))

    def find_recent_members(self, limit: int = 5):
        return self.model.objects.order_by("-membership_date")[:limit]
