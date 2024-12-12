from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Beer, Order, Review, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Beer, Cart, CartItem, Order, OrderItem



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


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    # Calculate total price for each item and grand total
    for item in items:
        item.total_price = item.quantity * item.beer.price  # Add total_price dynamically

    grand_total = sum(item.quantity * item.beer.price for item in items)

    return render(request, 'beer_shop/cart.html', {'cart': cart, 'items': items, 'grand_total': grand_total})



@login_required
def add_to_cart(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, beer=beer)
    if not created:
        cart_item.quantity += int(request.POST.get('quantity', 1))
    else:
        cart_item.quantity = int(request.POST.get('quantity', 1))
    cart_item.save()
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.exists():
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0
        for item in cart.items.all():
            if item.beer.stock >= item.quantity:
                # Create order items
                OrderItem.objects.create(order=order, beer=item.beer, quantity=item.quantity)
                # Decrease stock
                item.beer.stock -= item.quantity
                item.beer.save()
                # Add to total price
                total_price += item.beer.price * item.quantity
            else:
                # Handle insufficient stock (optional)
                pass
        order.total_price = total_price
        order.save()
        # Clear the cart
        cart.items.all().delete()
    return redirect('order_list')


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'beer_shop/order_list.html', {'orders': orders})

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # If quantity is 0, remove the item
    return redirect('cart')

@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')
