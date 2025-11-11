from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterable, Optional, TypeVar

from django.db.models import Q

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    """Abstract base class for repositories."""

    @abstractmethod
    def get_all(self) -> Iterable[T]:
        pass

    @abstractmethod
    def get_by_id(self, pk: Any) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    def update(self, pk: Any, **kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, pk: Any) -> int:
        pass

    @abstractmethod
    def filter(self, **filters) -> Iterable[T]:
        pass

    @abstractmethod
    def search(
        self, *q_objects: Q, exclude: Optional[Dict[str, Any]] = None
    ) -> Iterable[T]:
        pass
