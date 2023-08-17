import pytest
from django.test import Client  #udaje przeglądarkę
from django.urls import reverse
from django.contrib.auth.models import User
from words_app.models import WordToLearn

#test środowiska testowego
# @pytest.mark.django_db
# def test_check_env():
#     assert True


@pytest.mark.django_db
def test_index():
    browser = Client()
    url = reverse('index')  #generowanie urla na podstawie nazwy widoku w urls
    response = browser.get(url)  #wchodzimy metodą get na url
    content = str(response.content)
    url_print = reverse('category_list')
    print(url_print)
    assert response.status_code == 200
    assert '<h1>Powodzenia!</h1>'  in content


@pytest.mark.django_db
def test_LearningDashboardView(user, word_to_learn_1):
    browser = Client()
    browser.force_login(user)  # Logowanie użytkownika w kliencie testowym
    url = reverse('learning_dashboard')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['upcoming_words'].count() == 1


@pytest.mark.django_db
def test_LearningDashboardView_2(user, word_to_learn_13):
    browser = Client()
    browser.force_login(user)  # Logowanie użytkownika w kliencie testowym
    url = reverse('learning_dashboard')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['upcoming_words'].count() == 5


@pytest.mark.django_db
def test_WordListView_303_unauth():
    browser = Client()
    url = reverse('word_list')
    response = browser.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('log_in'))


@pytest.mark.django_db
def test_WordListView(user, word_to_learn_13):
    browser = Client()
    browser.force_login(user)
    url = reverse('word_list')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['words_to_learn'].count() == len(word_to_learn_13)


@pytest.mark.django_db
def test_CategoryListView_302_unauth():
    browser = Client()
    url = reverse('category_list')
    response = browser.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('log_in'))


@pytest.mark.django_db
def test_CategoryListView_13(user, word_category_13):
    browser = Client()
    browser.force_login(user)
    url = reverse('category_list')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['categories'].count() == len(word_category_13)
    for category in word_category_13:
        assert category in response.context['categories']





#czy poprawny status code
#czy dane w kontekście są oczekiwanymi
