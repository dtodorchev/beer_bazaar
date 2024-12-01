from django.urls import path
from .views import EditProfileView, RegisterView
from users.views import CustomLogoutView

urlpatterns = [
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),

]
