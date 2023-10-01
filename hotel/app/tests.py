"""
App tests
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):

    """
    Views tests
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_home_page_view(self):
        """
        Test Homepage
        """
        response = self.client.get(reverse("HomePage"))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        """
        Test About page
        """
        response = self.client.get(reverse("aboutpage"))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        """
        Test Contact page
        """
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_user_log_sign_page_get(self):
        """
        Test User login sign up
        """
        response = self.client.get(reverse("userloginpage"))
        self.assertEqual(response.status_code, 200)

    def test_user_log_sign_page_post(self):
        """
        Test user
        """
        data = {"email": "testuser", "pswd": "testpassword"}
        response = self.client.post(reverse("userloginpage"), data)
        self.assertEqual(
            response.status_code, 302
        )  # Assuming it redirects upon successful login

    def test_user_sign_up(self):
        """
        Test user creation
        """
        data = {
            "username": "newuser",
            "password1": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(reverse("usersignup"), data)
        self.assertEqual(
            response.status_code, 302
        )  # Assuming it redirects after successful signup

    # ... and so on for other views

    def tearDown(self):
        """
        Test user delete
        """
        self.user.delete()
