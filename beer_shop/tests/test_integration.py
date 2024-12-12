from django.test import TestCase
from django.urls import reverse
from beer_shop.models import Beer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from beer_shop.models import Beer, Category


class BeerListIntegrationTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Test Category")

        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # Minimal valid GIF binary data
            content_type='image/gif'
        )
        # Add a beer using the model directly (simulating admin behavior)
        self.beer = Beer.objects.create(
            name="Test Beer",
            brand="Test Brand",
            description="Test Description",
            price=5.99,
            alcohol_content=5.0,
            stock=10,
            category=self.category,
            image=self.test_image
        )

    def test_beer_list_view(self):
        # Test if the beer list view works and contains the beer data
        response = self.client.get(reverse('beer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beer_shop/beer_list.html')
        self.assertContains(response, 'Test Beer')


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserIntegrationTest(TestCase):
    def test_user_registration_and_login(self):
        # Register a new user
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login or home
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Log in the newly created user
        login_response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'strongpassword123',
        })
        self.assertEqual(login_response.status_code, 302)  # Redirect after login

        # Access a protected page (e.g., profile edit page)
        protected_response = self.client.get(reverse('edit_profile'))
        self.assertEqual(protected_response.status_code, 200)  # Should be accessible
        self.assertContains(protected_response, "Edit Your Profile")

from django.test import TestCase
from django.urls import reverse
from beer_shop.models import Beer, Cart, CartItem
from django.contrib.auth.models import User

class ShoppingCartIntegrationTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log the user in
        self.client.login(username='testuser', password='testpassword')
        # Create a category
        self.category = Category.objects.create(name="Test Category")
        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # Minimal valid GIF binary data
            content_type='image/gif'
        )
        # Create a beer
        self.beer = Beer.objects.create(
            name="Cart Test Beer",
            brand="Test Brand",
            description="A beer for testing",
            price=12.99,
            alcohol_content=5.0,
            stock=20,
            category=self.category,
            image=self.test_image
        )

    def test_add_to_cart(self):
        # Add beer to cart with quantity 2
        response = self.client.post(reverse('add_to_cart', args=[self.beer.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart

        # Check if the cart item exists and the quantity is correct
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, beer=self.beer)
        self.assertEqual(cart_item.quantity, 2)  # Ensure the quantity is updated


    def test_update_cart(self):
        # Add beer to cart
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, beer=self.beer, quantity=2)

        # Update the quantity
        response = self.client.post(reverse('update_cart_item', args=[cart_item.id]), {'quantity': 5})
        self.assertEqual(response.status_code, 302)  # Redirect after updating
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_remove_from_cart(self):
        # Add beer to cart
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, beer=self.beer, quantity=2)

        # Remove the item
        response = self.client.get(reverse('delete_cart_item', args=[cart_item.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after removing
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())
