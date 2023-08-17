"""
URL configuration for homework_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from words_app import views

urlpatterns = [
    path('word_list/', views.WordListView.as_view(), name='word_list'),
    path('word_add/', views.WordAddView.as_view(), name='word_add'),
    path('word_update/<int:id>', views.WordUpdateView.as_view(), name='word_update'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_delete/<int:id>', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('word_delete/<int:id>', views.WordToLearnDeleteView.as_view(), name='word_delete'),
    path('learning_dashboard/', views.LearningDashboardView.as_view(), name='learning_dashboard'),

]