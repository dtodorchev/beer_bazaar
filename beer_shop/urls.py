from django.urls import path
from . import views
from .views import AboutContactPageView, update_cart_item, delete_cart_item
from .views import cart_view, add_to_cart, checkout_view

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('beers/', views.BeerListView.as_view(), name='beer_list'),
    path('beers/<int:pk>/', views.BeerDetailView.as_view(), name='beer_detail'),
    path('orders/', views.UserOrderListView.as_view(), name='order_list'),
    path('beers/<int:pk>/review/', views.ReviewCreateView.as_view(), name='add_review'),

    path('about-contact/', AboutContactPageView.as_view(), name='about_contact'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:beer_id>/', add_to_cart, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),

    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),

]
