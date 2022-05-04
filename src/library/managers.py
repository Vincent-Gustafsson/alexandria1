from django.db import models


class ActiveBookLoanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(return_date__isnull=True)


class InactiveBookLoanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(return_date__isnull=False)
