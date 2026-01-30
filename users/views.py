from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from exchange.models import ImpactLog
from .forms import ProfileForm
from .models import Profile


@login_required
def profile(request):
    """
    Display the logged-in user's profile and a quick impact snapshot.
    """

    # Ensure a profile exists
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    impact_agg = ImpactLog.objects.filter(user=request.user).aggregate(
        total_items=Sum("items_kept_in_circulation"),
        total_co2=Sum("co2_saved_kg"),
    )

    context = {
        "profile": profile_obj,
        "impact_total_items": impact_agg.get("total_items") or 0,
        "impact_total_co2": impact_agg.get("total_co2") or 0.0,
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):
    """
    Allow users to update their profile details.
    """

    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, "users/edit_profile.html", {"form": form})


def password_reset(request):
    """
    Lightweight placeholder page to explain how to reset a password.
    For a real deployment, you would use Django's auth password reset views.
    """

    return render(request, "users/password_reset.html")

