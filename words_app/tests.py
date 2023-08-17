import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from .models import EngWord, PolWord, WordContext, WordCategory, WordToLearn
from .views import WordAddView





@pytest.mark.django_db
def test_word_add_view_get(client, user, word_category):
    client.force_login(user)
    response = client.get(reverse('word_add'))

    assert response.status_code == 200
    assert response.context['categories'].count() == 1
    assert response.context['categories'][0] == word_category

@pytest.mark.django_db
def test_word_add_view_post(client, user, word_category):
    client.force_login(user)
    post_data = {
        'eng_word': 'test_eng_word',
        'pol_word': 'test_pol_word',
        'text': 'test_text',
        'categories': [word_category.id],
    }
    response = client.post(reverse('word_add'), data=post_data)

    assert response.status_code == 302
    assert response.url == reverse('word_list')

    assert EngWord.objects.count() == 1
    assert PolWord.objects.count() == 1
    assert WordContext.objects.count() == 1
    assert WordToLearn.objects.count() == 1

    word_to_learn = WordToLearn.objects.first()
    assert word_to_learn.eng_word.word == 'test_eng_word'
    assert word_to_learn.pol_word.word == 'test_pol_word'
    assert word_to_learn.word_context.text == 'test_text'
    assert word_to_learn.member == user
    assert word_to_learn.category.count() == 1
    assert word_to_learn.category.first() == word_category





@pytest.mark.django_db
def test_word_list_view_get(client, user, word_to_learn):
    client.force_login(user)
    response = client.get(reverse('word_list'))

    assert response.status_code == 200
    assert response.context['words_to_learn'].count() == 1
    assert response.context['words_to_learn'][0] == word_to_learn

@pytest.mark.django_db
def test_word_list_view_post(client, user, word_to_learn):
    client.force_login(user)
    post_data = {
        'arrow': '↑',
        'search': '',
        'search_lang': 'eng',
        'repeat': '',
    }
    response = client.post(reverse('word_list'), data=post_data)

    assert response.status_code == 200








@pytest.mark.django_db
def test_word_update_view_get(client, user, word_to_learn, word_category):
    client.force_login(user)
    response = client.get(reverse('word_update', args=[word_to_learn.pk]))

    assert response.status_code == 200
    assert response.context['word_to_learn'] == word_to_learn
    assert response.context['categories'].count() == 1
    assert response.context['categories'][0] == word_category

@pytest.mark.django_db
def test_word_update_view_post(client, user, word_to_learn, word_category):
    client.force_login(user)
    post_data = {
        'eng_word': 'updated_eng_word',
        'pol_word': 'updated_pol_word',
        'text': 'updated_text',
        'memory_level': 3,
        'categories': [word_category.id],
    }
    response = client.post(reverse('word_update', args=[word_to_learn.pk]), data=post_data)

    assert response.status_code == 302
    assert response.url == reverse('word_list')

    # Check if the objects were updated
    word_to_learn.refresh_from_db()
    assert word_to_learn.eng_word.word == 'updated_eng_word'
    assert word_to_learn.pol_word.word == 'updated_pol_word'
    assert word_to_learn.word_context.text == 'updated_text'
    assert word_to_learn.memory_level == 3
    assert word_to_learn.category.count() == 1
    assert word_to_learn.category.first() == word_category





@pytest.mark.django_db
def test_category_list_view_get(client, user, word_category):
    client.force_login(user)
    response = client.get(reverse('category_list'))

    assert response.status_code == 200
    assert response.context['categories'].count() == 1
    assert response.context['categories'][0] == word_category

@pytest.mark.django_db
def test_category_list_view_post(client, user):
    client.force_login(user)
    post_data = {
        'new_category': 'new_test_category',
        'search': '',
    }
    response = client.post(reverse('category_list'), data=post_data)

    assert response.status_code == 200
    assert WordCategory.objects.filter(user=user, name='new_test_category').exists()

@pytest.mark.django_db
def test_category_list_view_search(client, user, word_category):
    client.force_login(user)
    post_data = {
        'new_category': '',
        'search': 'test_category',
    }
    response = client.post(reverse('category_list'), data=post_data)

    assert response.status_code == 200
    assert response.context['categories'].count() == 1
    assert response.context['categories'][0] == word_category




@pytest.mark.django_db
def test_category_delete_view(client, user, word_category):
    client.force_login(user)
    response = client.get(reverse('category_delete', args=[word_category.pk]))

    assert response.status_code == 302
    assert response.url == reverse('category_list')
    assert not WordCategory.objects.filter(pk=word_category.pk).exists()



@pytest.mark.django_db
def test_word_to_learn_delete_view(client, user, word_to_learn):
    client.force_login(user)
    response = client.get(reverse('word_delete', args=[word_to_learn.pk]))

    assert response.status_code == 302
    assert response.url == reverse('word_list')
    assert not WordToLearn.objects.filter(pk=word_to_learn.pk).exists()


@pytest.mark.django_db
def test_LearningDashboardView(client, user, word_to_learn):
    client.force_login(user)  # Logowanie użytkownika w kliencie testowym
    url = reverse('learning_dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['upcoming_words'].count() == 1


@pytest.mark.django_db
def test_LearningDashboardView_2(user, client, word_to_learn_13):
    client.force_login(user)  # Logowanie użytkownika w kliencie testowym
    url = reverse('learning_dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['upcoming_words'].count() == 5

