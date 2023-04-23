from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('quiz/', views.create_quiz, name='quiz'),
    path('quiz/<int:quiz_id>/', views.create_quiz, name='quiz'),
    path('play/', views.play, name='play'),
    path('myquizzes/', views.my_quizzes, name='my_quizzes'),
    
    path('category/create/', views.create_category, name='create_category'),
    path('category/get/', views.get_category, name='get_category'),
    path('category/remove/', views.remove_category, name='remove_category'),

    path('quiz/create/', views.set_quiz, name='create_quiz'),
    path('quiz/edit/', views.edit_quiz, name='edit_quiz'),

    path('question/create/', views.create_question, name='create_question'),
    path('question/get/all', views.get_question_all, name='get_question_all'),
    path('question/get/id', views.get_question_id, name='get_question_id'),
    path('question/remove/', views.remove_question, name='remove_question'),
    path('question/edit/', views.edit_question, name='edit_question'),
]