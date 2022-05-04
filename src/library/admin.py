from django.contrib import admin
from .models import Book, Copy, BookLoan, Author, Genre

class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ["title",]


class CopyAdmin(admin.ModelAdmin):
    model = Copy
    list_display = ["uid", "book"]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ["uid"]
        form = super(CopyAdmin, self).get_form(request, obj, **kwargs)
        return form


class BookLoanAdmin(admin.ModelAdmin):
    model = BookLoan
    list_display = ["copy", "user", "is_returned"]

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

    def is_returned(self, obj):
        return obj.return_date is not None

    is_returned.boolean = True


class AuthorAdmin(admin.ModelAdmin):
    model = Author


class GenreAdmin(admin.ModelAdmin):
    model = Genre


admin.site.register(Book, BookAdmin)
admin.site.register(Copy, CopyAdmin)
admin.site.register(BookLoan, BookLoanAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)