from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.contrib.auth.views import LogoutView

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['avatar', 'phone_number', 'address']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')



class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
