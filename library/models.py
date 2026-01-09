from django.db import models
from django.contrib.auth.models import User
from books.models import Book, Category

class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-added_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.name}"