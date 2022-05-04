from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string

from library.managers import ActiveBookLoanManager, InactiveBookLoanManager


User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Copy(models.Model):
    class Meta:
        verbose_name_plural = "copies"

    uid = models.CharField(unique=True, max_length=8, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.uid:
            generated_uid = get_random_string(8)
            while Copy.objects.filter(uid=generated_uid).exists():
                generated_uid = get_random_string(8)

            self.uid = generated_uid.upper()

        super(Copy, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - {self.uid}"


class BookLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active_loans = ActiveBookLoanManager()
    inactive_loans = InactiveBookLoanManager()

    def __str__(self):
        return f"{self.copy.uid} - {self.user.email}"

    @property
    def is_late(self):
        if self.due_date > timezone.now():
            return False
        
        return True
        
