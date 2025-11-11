from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import BookServiceException, NotFound
from .repositories.author_repository import AuthorRepository
from .repositories.book_repository import BookRepository
from .repositories.loan_repository import LoanRepository
from .repositories.member_repository import MemberRepository
from .serializers import (AuthorSerializer, BookSerializer, LoanSerializer,
                          MemberSerializer)
from .services.book_service import BookService
from .services.loan_service import LoanService
from .services.member_service import MemberService


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
    queryset = MemberRepository().get_all()
    serializer_class = MemberSerializer
    service = MemberService()

    @action(detail=False, methods=["get"], url_name="top-active", url_path="top-active")
    def top_active(self):
        top_active_members = self.service.get_top_active_memebers()


class LoanViewSet(viewsets.ModelViewSet):
    queryset = LoanRepository().get_all()
    serializer_class = LoanSerializer
    service = LoanService()

    @action(detail=True, methods=["post"])
    def extend_due_date(self, request, pk=None):
        loan_id = pk
        additional_days = request.data.get("additional_days")
        if not additional_days:
            return Response(
                {"Field error": "You need to send additional days for loan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            loan = self.service.extend_loan_additional_days(
                loan_id=loan_id, additional_days=additional_days
            )

        except BookServiceException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "status": "True",
                "details": "Loan's return date extended",
                "loan": loan.__dict__,
            },
            status=status.HTTP_200_OK,
        )
