from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .repositories.author_repository import AuthorRepository
from .repositories.book_repository import BookRepository
from .repositories.loan_repository import LoanRepository
from .repositories.member_repository import MemberRepository
from .serializers import (AuthorSerializer, BookSerializer, LoanSerializer,
                          MemberSerializer)
from .tasks import send_loan_notification


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = AuthorRepository().get_all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = BookRepository().get_all()
    serializer_class = BookSerializer
    service = BookService()

    @action(detail=True, methods=["post"])
    def loan(self, request, pk=None):
        member_id = request.data.get("member_id")
        try:
            loan = self.service.loan_book(pk, member_id)
            return Response(
                {"status": "Book loaned successfully.", "loan_id": loan.id},
                status=status.HTTP_201_CREATED,
            )
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BookServiceException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        member_id = request.data.get("member_id")
        try:
            loan = self.service.return_book(pk, member_id)
            return Response(
                {"status": "Book returned successfully.", "loan_id": loan.id},
                status=status.HTTP_200_OK,
            )
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BookServiceException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = MemberRepository.get_all()
    serializer_class = MemberSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = LoanRepository.get_all()
    serializer_class = LoanSerializer
