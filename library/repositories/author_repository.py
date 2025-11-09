from django.db.models import Q

from core.repositories.base_repository import BaseRepository
from library.models import Author


class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(Author)

    def find_by_name(self, name: str):
        return self.search(Q(first_name__icontains=name) | Q(last_name__icontains=name))
