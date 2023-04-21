from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    path('category/create/', views.create_category, name='create_category'),
    path('category/get/', views.get_category, name='get_category'),
    path('category/remove/', views.remove_category, name='remove_category'),

    path('quiz/create/', views.set_quiz, name='create_quiz'),
]