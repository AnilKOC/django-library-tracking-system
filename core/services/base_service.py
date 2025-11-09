from typing import Generic, Iterable, Optional, TypeVar

from django.db import transaction

from core.repositories.abstract_repository import AbstractRepository

from .abstract_service import AbstractService

T = TypeVar("T")


class BaseService(AbstractService[T], Generic[T]):
    """Generic base service implementing basic CRUD operations."""

    def __init__(self, repository: AbstractRepository[T]):
        self.repo = repository

    def list(self) -> Iterable[T]:
        return self.repo.get_all()

    def get(self, pk: int) -> Optional[T]:
        return self.repo.get_by_id(pk)

    def create(self, **kwargs) -> T:
        return self.repo.create(**kwargs)

    def update(self, pk: int, **kwargs) -> Optional[T]:
        return self.repo.update(pk, **kwargs)

    def delete(self, pk: int) -> bool:
        deleted = self.repo.delete(pk)
        return deleted > 0
