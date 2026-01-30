from django.urls import path

from . import views


urlpatterns = [
    path("browse/", views.browse_items, name="browse"),
    path("items/<int:pk>/", views.item_detail, name="item_detail"),
    path("items/new/", views.create_item, name="create_item"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("eco-finder/", views.eco_finder, name="eco_finder"),
    path("community/", views.community, name="community"),
]

