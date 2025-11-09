from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


class AbstractService(ABC, Generic[T]):
    """Abstract base class for services."""

    @abstractmethod
    def list(self) -> Iterable[T]:
        pass

    @abstractmethod
    def get(self, pk: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    def update(self, pk: int, **kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, pk: int) -> bool:
        pass
