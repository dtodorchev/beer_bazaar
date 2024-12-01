from django.urls import path
from . import views
from .views import  AboutContactPageView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('beers/', views.BeerListView.as_view(), name='beer_list'),
    path('beers/<int:pk>/', views.BeerDetailView.as_view(), name='beer_detail'),
    path('orders/', views.UserOrderListView.as_view(), name='order_list'),
    path('beers/<int:pk>/review/', views.ReviewCreateView.as_view(), name='add_review'),

    path('about-contact/', AboutContactPageView.as_view(), name='about_contact'),

]
