from django.test import TestCase
from users.forms import CustomUserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        # Set up a user for testing duplicate username validation
        self.existing_user = User.objects.create_user(username='existing_user', email='existing@example.com', password='password123')

    def test_valid_form(self):
        form_data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_username(self):
        form_data = {
            'username': 'existing_user',  # This username already exists
            'email': 'duplicate@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], "A user with that username already exists.")

    def test_passwords_do_not_match(self):
        form_data = {
            'username': 'another_user',
            'email': 'another_user@example.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword456',  # Passwords do not match
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_email(self):
        form_data = {
            'username': 'invalid_email_user',
            'email': 'not-an-email',  # Invalid email format
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
