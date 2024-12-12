from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from beer_shop.models import Beer, Category

class BeerModelTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Test Category")

        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # Minimal binary data for a GIF file
            content_type='image/gif'
        )

        # Create a Beer object with all required fields, including image
        self.beer = Beer.objects.create(
            name="Test Beer",
            brand="Test Brand",
            description="Test Description",
            price=5.99,
            alcohol_content=5.0,
            stock=10,
            category=self.category,  # Associate the beer with the test category
            image=self.test_image  # Provide the test image
        )

    def test_beer_creation(self):
        # Check basic fields
        self.assertEqual(self.beer.name, "Test Beer")
        self.assertEqual(self.beer.price, 5.99)
        self.assertEqual(self.beer.alcohol_content, 5.0)
        self.assertEqual(self.beer.stock, 10)
        self.assertEqual(self.beer.category.name, "Test Category")  # Check category association

        # Check the image path
        self.assertTrue(self.beer.image.name.startswith(
            'static/beer_images/test_image'))  # Check that the image path starts with the expected prefix

    def test_str_method(self):
        # Verify the __str__ method of the Beer model
        self.assertEqual(str(self.beer), "Test Beer")
