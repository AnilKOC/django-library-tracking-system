class BookServiceException(Exception):
    """Base exception for book service errors (400 Bad Request)."""

    pass


class NotFound(BookServiceException):
    """Base class for 404 Not Found exceptions."""

    pass


class BookNotFound(NotFound):
    """Book not found (404)."""

    pass


class MemberNotFound(NotFound):
    """Member not found (404)."""

    pass


class ActiveLoanNotFound(NotFound):
    """Active loan not found (404)."""

    pass


class NoAvailableCopies(BookServiceException):
    """No copies available (400)."""

    pass
