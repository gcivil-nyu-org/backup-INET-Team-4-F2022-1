from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from main.forms import NewUserForm

# class for base tests to generate users, etc. for tests below
# called once before each case is run good place to store testing data


class BaseTest(TestCase):
    def setUp(self):
        # url used for homepage
        self.homepage_url = reverse("main:homepage")
        # url used to produce response for register
        self.register_url = reverse("main:register")
        # url used to produce response for login
        self.login_url = reverse("main:login")
        # url used to logout
        self.logout_url = reverse("main:logout")

        # some test users
        self.user = {
            "username": "testuser3",
            "email": "testemail@gmail.com",
            "password1": "UncxYv234zzy",
            "password2": "UncxYv234zzy",
        }
        self.invalid_user = {
            "username": "",
            "email": "testemail@gmail.com",
            "password1": "pwd",
            "password2": "pwd",
        }

        return super().setUp()


class HomePageTest(BaseTest):
    def test_homepage_access(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")


class RegisterTest(BaseTest):
    def test_register_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/register.html")

    def test_register_success_url(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 302)

    def test_register_form_valid(self):
        form_data = self.user
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = self.invalid_user
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_registration(self):
        self.client.post(self.register_url, self.invalid_user, format="text/html")
        user = User.objects.filter(username=self.user["username"]).first()
        self.assertEqual(user, None)


# tests for login
class LoginTest(BaseTest):
    def test_login_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/login.html")

    # should be re-direct in future
    def test_login_success_url(self):
        self.client.post(self.register_url, self.user, format="text/html")
        user = User.objects.filter(username=self.user["username"]).first()
        user.save()
        response = self.client.post(self.login_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)

    def test_client_login(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        self.assertTrue(logged_in)


class LogoutTest(BaseTest):
    # test for redirect to homepage
    def test_logout_url(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)