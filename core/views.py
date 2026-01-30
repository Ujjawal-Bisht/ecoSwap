from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from exchange.models import Item


def home(request):
    """
    Landing page with a brief explanation and a few featured items.
    """

    featured_items = Item.objects.filter(is_active=True).select_related("category")[:5]
    return render(request, "home.html", {"items": featured_items})

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def faq(request):
    return render(request, "core/faq.html")

def terms(request):
    return render(request, "core/terms.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-log in new users for a smoother experience
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "users/login.html", {"msg": "Invalid credentials!"}
            )
    return render(request, "users/login.html", {"form": AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect("home")