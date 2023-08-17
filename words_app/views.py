from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from words_app.models import PolWord, EngWord, WordContext
from words_app.models import WordToLearn, WordContext, EngWord, PolWord, WordCategory
from django.utils import timezone
from django.urls import reverse




class WordAddView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        categories = WordCategory.objects.filter(user=user)
        return render(request, 'words_app/word_add_form.html', {'categories': categories})

    def post(self, request):
        eng_word_get = request.POST.get('eng_word')
        pol_word_get = request.POST.get('pol_word')
        text_get = request.POST.get('text')
        categories_selected = request.POST.getlist('categories')
        user = request.user

        eng_word = EngWord.objects.create(word=eng_word_get)
        pol_word = PolWord.objects.create(word=pol_word_get)
        text = WordContext.objects.create(text=text_get)

        next_repeat = timezone.now() + timezone.timedelta(days=1)

        word_to_learn = WordToLearn.objects.create(
            member=user,
            eng_word=eng_word,
            pol_word=pol_word,
            word_context=text,
            memory_level=1,
            next_repeat=next_repeat
        )

        for cat_id in categories_selected:
            category = WordCategory.objects.get(pk=cat_id)
            word_to_learn.category.add(category)

        return redirect('word_list')


class WordListView(View):
    @method_decorator(login_required)
    def get(self, request):
        words_to_learn = WordToLearn.objects.filter(member=request.user)
        return render(request, 'words_app/word_list.html', {'words_to_learn': words_to_learn})

    def post(self, request):
        user = request.user
        words_to_learn = WordToLearn.objects.filter(member=user)
        arrow = request.POST.get('arrow')
        repeat = request.POST.get('repeat')
        search = request.POST.get('search')
        search_lang = request.POST.get('search_lang')
        print(search_lang)



        if search:
            if search_lang == 'eng':
                words_to_learn = WordToLearn.objects.filter(member=user, eng_word__word__icontains=search)
            if search_lang == 'pol':
                words_to_learn = WordToLearn.objects.filter(member=user, pol_word__word__icontains=search)


        if arrow == '↑':
            words_to_learn = WordToLearn.objects.filter(member=user).select_related('eng_word').order_by(
                                                                                                    '-memory_level',
                                                                                                     'eng_word__word')
        elif arrow == '↓':
            words_to_learn = WordToLearn.objects.filter(member=user).select_related('eng_word').order_by(
                                                                                                    'memory_level',
                                                                                                    'eng_word__word')
        elif repeat == '↑':
            words_to_learn = WordToLearn.objects.filter(member=user).select_related('eng_word').order_by('-next_repeat')

        elif repeat == '↓':
            words_to_learn = WordToLearn.objects.filter(member=user).select_related('eng_word').order_by('next_repeat')

        return render(request, 'words_app/word_list.html', {'words_to_learn': words_to_learn})


class WordUpdateView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        word_to_learn = WordToLearn.objects.get(pk=id)
        user = request.user
        categories = WordCategory.objects.filter(user=user)
        return render(request, 'words_app/word_update_form.html', {'word_to_learn': word_to_learn,
                                                                   'categories': categories})

    def post(self, request, id):
        eng_word = request.POST.get('eng_word')
        pol_word = request.POST.get('pol_word')
        text = request.POST.get('text')
        memory_level = request.POST.get('memory_level')
        categories_selected = request.POST.getlist('categories')

        word_to_learn = WordToLearn.objects.get(pk=id)

        word_to_learn.eng_word.word = eng_word
        word_to_learn.eng_word.save()
        word_to_learn.pol_word.word = pol_word
        word_to_learn.pol_word.save()
        word_to_learn.word_context.text = text
        word_to_learn.word_context.save()
        word_to_learn.memory_level = memory_level
        word_to_learn.save()

        for cat_id in categories_selected:
            category = WordCategory.objects.get(pk=cat_id)
            word_to_learn.category.add(category)


        return redirect('word_list')


class CategoryListView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        categories = WordCategory.objects.filter(user=user)
        return render(request, 'words_app/category_list.html', {'categories': categories})

    def post(self, request):
        user = request.user
        new_category = request.POST.get('new_category')
        search = request.POST.get('search')
        categories = WordCategory.objects.filter(user=user)

        if new_category:
            WordCategory.objects.create(user=user, name=new_category)

        if search:
            categories = WordCategory.objects.filter(user=user, name__icontains=search)

        return render(request, 'words_app/category_list.html', {'categories': categories})

class CategoryDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        user = request.user

        category = WordCategory.objects.get(id=id, user=user)
        category.delete()
        return redirect('category_list')


class WordToLearnDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        word_to_learn = WordToLearn.objects.get(id=id)
        word_to_learn.delete()
        return redirect('word_list')


class LearningDashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        upcoming_words = WordToLearn.objects.filter(member=user).order_by('next_repeat')
        upcoming_words = upcoming_words[:5]
        low_memory_level = WordToLearn.objects.filter(member=user).order_by('memory_level')
        low_memory_level = low_memory_level[:5]

        return render(request, 'words_app/learning_dashboard.html', {'upcoming_words': upcoming_words,
                                                                     'low_memory_level': low_memory_level})



