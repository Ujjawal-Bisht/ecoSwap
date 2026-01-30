from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
]