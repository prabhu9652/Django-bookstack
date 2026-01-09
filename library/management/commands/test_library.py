from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book
from library.models import UserLibrary

class Command(BaseCommand):
    help = 'Test library functionality'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass')
            user.save()
            self.stdout.write(f'Created test user: {user.username}')
        else:
            self.stdout.write(f'Using existing user: {user.username}')

        # Get a test book
        book = Book.objects.first()
        if not book:
            self.stdout.write(self.style.ERROR('No books found in database'))
            return

        self.stdout.write(f'Testing with book: {book.name}')

        # Test adding book to library
        library_item, created = UserLibrary.objects.get_or_create(
            user=user,
            book=book
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully added book to library'))
        else:
            self.stdout.write(self.style.WARNING(f'Book already in library'))

        # Test removing book from library
        UserLibrary.objects.filter(user=user, book=book).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully removed book from library'))

        # Test adding again
        library_item = UserLibrary.objects.create(user=user, book=book)
        self.stdout.write(self.style.SUCCESS(f'Successfully added book to library again'))

        # Show library count
        count = UserLibrary.objects.filter(user=user).count()
        self.stdout.write(f'User library now has {count} books')