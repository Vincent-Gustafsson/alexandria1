from django.urls import path

from .views import dashboard_view, loan_book, return_book


app_name = "library"

urlpatterns = [
    path("dashboard", dashboard_view, name="dashboard"),
    path("loan", loan_book, name="loan"),
    path("return", return_book, name="return"),
]
