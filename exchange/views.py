from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, SwapRequestForm
from .models import CommunityPost, EcoPlace, ImpactLog, Item


def browse_items(request):
    """
    Public browse page for active items.
    """

    items = Item.objects.filter(is_active=True).select_related("category", "owner")[:50]
    return render(request, "exchange/browse_items.html", {"items": items})


@login_required
def create_item(request):
    """
    Allow a logged-in user to list a new item.
    """

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect("dashboard")
    else:
        form = ItemForm()
    return render(request, "exchange/create_item.html", {"form": form})


def item_detail(request, pk):
    """
    Simple item detail with optional swap request form.
    """

    item = get_object_or_404(Item, pk=pk, is_active=True)
    swap_form = None

    if request.user.is_authenticated and request.user != item.owner:
        if request.method == "POST":
            swap_form = SwapRequestForm(request.POST)
            if swap_form.is_valid():
                swap_request = swap_form.save(commit=False)
                swap_request.item = item
                swap_request.from_user = request.user
                swap_request.save()
                return redirect("item_detail", pk=item.pk)
        else:
            swap_form = SwapRequestForm()

    context = {
        "item": item,
        "swap_form": swap_form,
    }
    return render(request, "exchange/item_detail.html", context)


@login_required
def dashboard(request):
    """
    User-centric dashboard showing their items and a simple impact summary.
    """

    items = Item.objects.filter(owner=request.user).select_related("category")
    impact_agg = ImpactLog.objects.filter(user=request.user).aggregate(
        total_items=Sum("items_kept_in_circulation"),
        total_co2=Sum("co2_saved_kg"),
    )

    context = {
        "items": items,
        "impact_total_items": impact_agg.get("total_items") or 0,
        "impact_total_co2": impact_agg.get("total_co2") or 0.0,
    }
    return render(request, "exchange/dashboard.html", context)


def eco_finder(request):
    """
    List eco infrastructure locations, optionally filtered by city or type.
    """

    city = request.GET.get("city", "").strip()
    place_type = request.GET.get("type", "").strip()

    places = EcoPlace.objects.all()
    if city:
        places = places.filter(city__icontains=city)
    if place_type:
        places = places.filter(place_type=place_type)

    return render(
        request,
        "exchange/eco_finder.html",
        {
            "places": places,
            "selected_city": city,
            "selected_type": place_type,
        },
    )


def community(request):
    """
    Simple community feed of sustainability stories and tips.
    """

    posts = CommunityPost.objects.select_related("author")[:50]

    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()
        if title and body:
            CommunityPost.objects.create(author=request.user, title=title, body=body)
            return redirect("community")

    return render(request, "exchange/community.html", {"posts": posts})

