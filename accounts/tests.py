import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.views import RegisterView

@pytest.mark.django_db
def test_register_view_get(client):
    response = client.get(reverse('register'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_register_view_post_success(client):
    post_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    response = client.post(reverse('register'), data=post_data)

    assert response.status_code == 200
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_register_view_post_mismatched_passwords(client):
    post_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'testuser',
        'password1': 'testpassword1',
        'password2': 'testpassword2',
    }

    response = client.post(reverse('register'), data=post_data)

    assert response.status_code == 200
    assert 'Hasła nie są takie same' in response.context['base_msg']

@pytest.mark.django_db
def test_register_view_post_existing_username(client):
    existing_user = User.objects.create_user(username='existinguser', password='existingpassword')

    post_data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'username': 'existinguser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }

    response = client.post(reverse('register'), data=post_data)

    assert response.status_code == 200
    assert 'Użytkownik o podanej nazwie już istnieje.' in response.context['base_msg']







@pytest.mark.django_db
def test_user_login_view_post_valid_credentials(client):
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)

    post_data = {
        'username': username,
        'password': password,
    }

    response = client.post(reverse('log_in'), data=post_data)

    assert response.status_code == 200
    assert f'Witaj {user}' in response.context['base_msg']

@pytest.mark.django_db
def test_user_login_view_post_invalid_credentials(client):
    post_data = {
        'username': 'nonexistentuser',
        'password': 'invalidpassword',
    }

    response = client.post(reverse('log_in'), data=post_data)

    assert response.status_code == 200
    assert 'Wprowadziłeś błędny login lub hasło, spróbuj jeszcze raz lub załóż nowe konto.' in response.context['base_msg']


