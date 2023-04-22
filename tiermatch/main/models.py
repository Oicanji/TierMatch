from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=20000)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    allow_allias = models.CharField(max_length=100)
    super_allow_allias = models.CharField(max_length=100)
    deny_allias = models.CharField(max_length=100)
    allow_color = models.CharField(max_length=7)
    deny_color = models.CharField(max_length=7)
    super_allow_color = models.CharField(max_length=7)
    
    list_answers = models.ManyToManyField('Question')
    list_categories = models.ManyToManyField('Category')

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    attribute = models.CharField(max_length=20000)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    categories_id = models.ForeignKey('Category', on_delete=models.CASCADE)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

class Answers(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    list_answers = models.ManyToManyField('Question', through='Answer')

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    id_answer = models.ForeignKey('Answers', on_delete=models.CASCADE)
    id_question = models.ForeignKey('Question', on_delete=models.CASCADE)
    id_category = models.ForeignKey('Category', on_delete=models.CASCADE)