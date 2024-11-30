from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Beer, Order, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = 'beer_shop/home.html'

class BeerListView(ListView):
    model = Beer
    template_name = 'beer_shop/beer_list.html'
    context_object_name = 'beers'  # Default is 'object_list'

class BeerDetailView(DetailView):
    model = Beer
    template_name = 'beer_shop/beer_detail.html'
    context_object_name = 'beer'  # Default is 'object'

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
