from django.db.models import Q

from core.repositories.base_repository import BaseRepository
from library.models import Book


class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(Book)

    def find_by_title(self, title: str):
        return self.filter(title__icontains=title)

    def find_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def find_available_books(self):
        return self.filter(available_copies__gt=0)

    def search_books(self, keyword: str):
        return self.search(
            Q(title__icontains=keyword)
            | Q(author__first_name__icontains=keyword)
            | Q(author__last_name__icontains=keyword)
        )
