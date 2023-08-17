import pytest
from django.contrib.auth.models import User
from words_app.models import WordToLearn
from words_app.models import PolWord, EngWord, WordContext, WordCategory


@pytest.fixture
def user():
    return User.objects.create_user(username='testowyZiomek', password='1234')

@pytest.fixture
def eng_word():
    return EngWord.objects.create(word='exampleword')

@pytest.fixture
def pol_word():
    return PolWord.objects.create(word='przykładowesłowo')

@pytest.fixture
def word_context():
    return WordContext.objects.create(text='Przykładowe zdanie')

@pytest.fixture
def word_category(user):
    return WordCategory.objects.create(user=user, name='PrzykładowaKategoria')

@pytest.fixture
def word_category_13(user):
    lst = []
    for x in range(13):
        lst.append(WordCategory.objects.create(user=user, name='PrzykładowaKategoria'))
    return lst


@pytest.fixture
def word_to_learn_1(user, eng_word, pol_word, word_context, word_category):
    lst = []
    for x in range(1):
        lst.append(
            WordToLearn.objects.create(
                member=user,
                eng_word=eng_word,
                pol_word=pol_word,
                word_context=word_context,
                memory_level=4,
                next_repeat='2023-10-10'
            ).category.add(word_category)
        )
    return lst


@pytest.fixture
def word_to_learn_13(user, eng_word, pol_word, word_context, word_category):
    lst = []
    for x in range(13):
        lst.append(
            WordToLearn.objects.create(
                member=user,
                eng_word=eng_word,
                pol_word=pol_word,
                word_context=word_context,
                memory_level=4,
                next_repeat='2023-10-10'
            ).category.add(word_category)
        )
    return lst



# @pytest.fixture
# def word_category_delete():
#