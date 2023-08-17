from django.db import models
from django.contrib.auth.models import User


class EngWord(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word


class PolWord(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word


class WordContext(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class WordCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WordToLearn(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    eng_word = models.ForeignKey(EngWord, on_delete=models.CASCADE)
    pol_word = models.ForeignKey(PolWord, on_delete=models.CASCADE)
    word_context = models.ForeignKey(WordContext, on_delete=models.SET_NULL, blank=True, null=True)
    memory_level = models.IntegerField(choices=[(i, i) for i in range(1, 10)])
    next_repeat = models.DateField(null=True, blank=True)
    category = models.ManyToManyField(WordCategory)

    def __str__(self):
        return f'{self.eng_word} - {self.pol_word}'


