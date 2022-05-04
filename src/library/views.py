import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render

from library.models import BookLoan, Copy


@login_required
def dashboard_view(request: HttpRequest):
    ctx = {}
    ctx["loans"] = BookLoan.active_loans.filter(user=request.user)
    return render(request, "dashboard.html", ctx)

def loan_book(request: HttpRequest):
    uid = request.POST.get("uid", False)
    if not uid:
        messages.error(request, "Dålig streckkod")
        return redirect("library:dashboard")
    
    try:
        copy = Copy.objects.get(uid=uid)
    except Copy.DoesNotExist:
        messages.error(request, "Dålig streckkod")
        return redirect("library:dashboard")
    
    if BookLoan.active_loans.filter(copy=copy).exists():
        messages.error(request, "Boken är redan lånad")
        return redirect("library:dashboard")
    
    loan = BookLoan.objects.create(
        copy=copy,
        user=request.user,
        due_date=timezone.now() + datetime.timedelta(weeks=3)
    )

    if loan.pk is None:
        messages.error(request, "Kunde inte låna bok, försök igen.")
        return redirect("library:dashboard")

    messages.success(request, f"Du har lånat {copy.book}")
    return redirect("library:dashboard")


def return_book(request: HttpRequest):
    uid = request.POST.get("uid", False)
    if not uid:
        messages.error(request, "Dålig streckkod")
        return redirect("library:dashboard")
    
    try:
        copy = Copy.objects.get(uid=uid)
    except Copy.DoesNotExist:
        messages.error(request, "Dålig streckkod")
        return redirect("library:dashboard")
    
    try:
        loan = BookLoan.active_loans.get(copy=copy)
    except BookLoan.DoesNotExist:
        messages.error(request, "Den här boken är olånad.")
        return redirect("library:dashboard")

    if loan.user != request.user:
        messages.error(request, "Den här boken är inte lånad av dig.")
        return redirect("library:dashboard")

    loan.return_date = timezone.now()
    loan.save()

    messages.success(request, f"Du har lämnat tillbaka {copy.book}")
    return redirect("library:dashboard")