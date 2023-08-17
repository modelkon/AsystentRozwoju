import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from accounts.views import RegisterView
@pytest.fixture
def client():
    from django.test.client import Client
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='existinguser', password='testpassword')