from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from beer_shop.models import Beer, Category

class BeerListViewTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Test Category")

        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # This is binary data for a minimal GIF file
            content_type='image/gif'
        )

        # Create a Beer object with the test image
        self.beer = Beer.objects.create(
            name="Test Beer",
            brand="Test Brand",
            description="Test Description",
            price=5.99,
            alcohol_content=5.0,
            stock=10,
            category=self.category,
            image=self.test_image  # Provide the test image
        )

    def test_beer_list_view(self):
        response = self.client.get(reverse('beer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beer_shop/beer_list.html')
        self.assertContains(response, 'Test Beer')
