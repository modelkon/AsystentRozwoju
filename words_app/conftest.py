import pytest
from django.contrib.auth.models import User
from .models import EngWord, PolWord, WordContext, WordCategory, WordToLearn

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def client():
    from django.test.client import Client
    return Client()

@pytest.fixture
def eng_word():
    return EngWord.objects.create(word='test_eng_word')

@pytest.fixture
def pol_word():
    return PolWord.objects.create(word='test_pol_word')

@pytest.fixture
def word_context():
    return WordContext.objects.create(text='test_text')

@pytest.fixture
def word_category(user):
    return WordCategory.objects.create(user=user, name='test_category')

@pytest.fixture
def word_to_learn(user, eng_word, pol_word, word_context, word_category):
    return WordToLearn.objects.create(
        member=user,
        eng_word=eng_word,
        pol_word=pol_word,
        word_context=word_context,
        memory_level=5,
        next_repeat='2023-08-10',
    )


@pytest.fixture
def word_to_learn_13(user, eng_word, pol_word, word_context, word_category):
    for x in range(13):
        WordToLearn.objects.create(
            member=user,
            eng_word=eng_word,
            pol_word=pol_word,
            word_context=word_context,
            memory_level=4,
            next_repeat='2023-10-10')
