import random
from datetime import date, timedelta

from django.contrib.auth.models import User

from library.models import (Author, Book,  # app adını kendine göre değiştir
                            Loan, Member)

# --- Yardımcı veriler ---
FIRST_NAMES = [
    "John",
    "Jane",
    "Alice",
    "Bob",
    "Michael",
    "Sarah",
    "Emma",
    "David",
    "Mark",
    "Olivia",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Taylor",
    "Anderson",
    "Clark",
    "Lee",
    "Walker",
    "Hall",
    "Young",
]
GENRES = ["fiction", "nonfiction", "sci-fi", "biography"]

BOOK_TITLES = [
    "The Silent Storm",
    "Journey Beyond the Stars",
    "Echoes of the Past",
    "Fragments of Tomorrow",
    "The Hidden Truth",
    "Mind over Matter",
    "The Edge of Infinity",
    "Memoirs of a Wanderer",
    "The Future Chronicles",
    "Under the Crimson Sky",
    "Artificial Souls",
    "Reflections of Reality",
]


def seed_authors(n=10):
    authors = []
    for _ in range(n):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        bio = f"{first_name} {last_name} is an acclaimed author known for their {random.choice(GENRES)} novels."
        author = Author.objects.create(
            first_name=first_name, last_name=last_name, biography=bio
        )
        authors.append(author)
    print(f"✅ {n} authors created.")
    return authors


def seed_books(authors, n=20):
    books = []
    for _ in range(n):
        title = random.choice(BOOK_TITLES) + f" Vol. {random.randint(1, 5)}"
        author = random.choice(authors)
        isbn = str(random.randint(1000000000000, 9999999999999))
        genre = random.choice(GENRES)
        copies = random.randint(1, 5)
        book = Book.objects.create(
            title=title, author=author, isbn=isbn, genre=genre, available_copies=copies
        )
        books.append(book)
    print(f"✅ {n} books created.")
    return books


def seed_members(n=10):
    members = []
    for i in range(n):
        username = f"user{i+1}"
        email = f"{username}@example.com"
        user = User.objects.create_user(
            username=username, email=email, password="test1234"
        )
        member = Member.objects.create(user=user)
        members.append(member)
    print(f"✅ {n} members created.")
    return members


def seed_loans(books, members, n=25):
    loans = []
    for _ in range(n):
        book = random.choice(books)
        member = random.choice(members)
        loan_date = date.today() - timedelta(days=random.randint(1, 30))
        return_date = loan_date + timedelta(days=random.randint(7, 20))
        is_returned = random.choice([True, False])

        loan = Loan.objects.create(
            book=book,
            member=member,
            loan_date=loan_date,
            return_date=return_date if is_returned else None,
            is_returned=is_returned,
        )

        # Eğer kitap teslim edilmediyse mevcut kopyayı azalt
        if not is_returned and book.available_copies > 0:
            book.available_copies -= 1
            book.save()

        loans.append(loan)
    print(f"✅ {n} loans created.")
    return loans


def run():
    print("Seeding data...")
    Author.objects.all().delete()
    Book.objects.all().delete()
    Member.objects.all().delete()
    Loan.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    authors = seed_authors(10)
    books = seed_books(authors, 20)
    members = seed_members(10)
    loans = seed_loans(books, members, 25)

    print("🎉 Seeding completed successfully!")


if __name__ == "__main__":
    run()
