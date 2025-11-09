from typing import Iterable, Optional, Type, TypeVar

from django.db import models

from .abstract_repository import AbstractRepository

T = TypeVar("T", bound=models.Model)


class BaseRepository(AbstractRepository[T]):
    """Generic base repository using Django ORM."""

    model: Type[T] = None

    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self) -> Iterable[T]:
        return self.model.objects.all()

    def get_by_id(self, pk: int, raise_exception: bool = False) -> Optional[T]:
        if raise_exception:
            return self.model.objects.get(pk=pk)
        return self.model.objects.filter(pk=pk).first()

    def create(self, **kwargs) -> T:
        instance = self.model.objects.create(**kwargs)
        return instance

    def update(self, pk: int, **kwargs) -> Optional[T]:
        updated = self.model.objects.filter(pk=pk).update(**kwargs)
        if updated:
            return self.model.objects.get(pk=pk)
        return None

    def delete(self, pk: int) -> int:
        deleted, _ = self.model.objects.filter(pk=pk).delete()
        return deleted

    def filter(self, **filters) -> Iterable[T]:
        return self.model.objects.filter(**filters)

    def search(self, *q_objects: Q, exclude: Optional[dict] = None) -> Iterable[T]:
        queryset = self.model.objects.filter(*q_objects)
        if exclude:
            queryset = queryset.exclude(**exclude)
        return queryset
