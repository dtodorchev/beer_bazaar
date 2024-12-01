from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Beer, Order, Review, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django import forms


class HomePageView(TemplateView):
    template_name = 'beer_shop/home.html'

class BeerListView(ListView):
    model = Beer
    template_name = 'beer_shop/beer_list.html'
    context_object_name = 'beers'

class BeerDetailView(DetailView):
    model = Beer
    template_name = 'beer_shop/beer_detail.html'
    context_object_name = 'beer'

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'beer_shop/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'beer_shop/add_review.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.beer_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('beer_detail', kwargs={'pk': self.kwargs['pk']})

def home(request):
    featured_beers = Beer.objects.order_by('-id')[:8]
    categories = Category.objects.all()
    return render(request, 'beer_shop/home.html', {
        'featured_beers': featured_beers,
        'categories': categories,
    })





class AboutContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class AboutContactPageView(FormView):
    template_name = 'beer_shop/about_contact.html'
    form_class = AboutContactForm
    success_url = reverse_lazy('about_contact')

    def form_valid(self, form):
        # Handle form submission (e.g., send email or log the message)
        print(form.cleaned_data)
        return super().form_valid(form)


