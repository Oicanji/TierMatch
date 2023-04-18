from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def index(request):
    return render(request, 'main/home.html', {})


@login_required
def cadastrar_quiz(request):
    quiz_id = request.GET.get('id')
    args = '{}'
    if quiz_id:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz:
            if quiz.user_id == request.user.id:
                args = {"code": 200, "response": quiz}
            else:
                args = {"code": 403, "response": "Você não tem permissão para editar esse quiz"}
        else:
            args = {"code": 404, "response": "Quiz não encontrado"}
    else:
        args = {"code": 400, "response": "Quiz não encontrado"}
            
    return args



"""
ROTA / PLAY
Rota que o usuário vai acessar para jogar o quiz
Tem que ser enviado o id do quiz caso contrário, envie para o acesso proibido
"""

"""
ROTA / GET / QUIZ
Quando o usuário quer buscar um quiz dentro do banco
Ele vai passar o id do quiz e vai retornar o quiz
"""

@login_required
def quiz(request):
    quiz_id = request.GET.get('id')
    args = '{}'
    if quiz_id:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz:
            args = {"code": 200, "response": quiz}
        else:
            args = {"code": 404, "response": "Quiz não encontrado"}
    else:
        args = {"code": 400, "response": "Quiz não encontrado"}
            
    return args



"""
ROTA / GET / QUIZZES
Quando o usuário quer buscar os quizzes dentro do banco
Pode ser passado uma chave 'like' para buscar por nome
Pode ser passado uma chave 'category' para buscar por categoria
Pode ser passado uma chave 'user' para buscar por usuário
Pode ser passado uma chave 'offset' para ser o index de onde vai começar a buscar caso contrário, vai ser 0
Pode ser passado uma chave 'limit' para ser o limite de resultados caso contrário, vai ser 50
Pode ser passado a ordenação dos resultados por id em ordem crescente ou decrescente apenas, por um parametro 'order_by'

Por default, ele vai ordenar os resultados por ordem decrescente de id
"""

"""
ROTA / SET / QUIZ
Rota de criação do quiz
Tem que ser passados os seguintes parametros:
name = nome do quiz
description = descrição do quiz
create_by = id do usuário que está criando o quiz

super_allow_alias = alias do super_allow
allow_alias = alias do allow
deny_alias = alias do deny

super_allow_color = cor do super_allow
allow_color = cor do allow
deny_color = cor do deny
"""


"""

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

create a routes get, set and remove for category 

"""
@login_required
def get_category(request):
    category_id = request.GET.get('id')
    args = '{}'
    if category_id:
        category = Category.objects.filter(id=category_id).first()
        if category:
            args = {"code": 200, "response": category}
        else:
            args = {"code": 404, "response": "Categoria não encontrada"}
    else:
        args = {"code": 400, "response": "Categoria não encontrada"}
    return args

@login_required
def create_category(request):
    args = '{}'
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color')
        if name and color:
            category = Category(name=name, color=color)
            category.save()
            args = {"code": 200, "response": category}
        else:
            args = {"code": 400, "response": "Categoria não encontrada"}
    else:
        args = {"code": 400, "response": "Categoria não encontrada"}
    return args

"""
ROTA / REMOVE / CATEGORY
Sim não é necessário editar uma categoria, apenas remover e criar uma nova
Tem que ser passado o id da categoria
Tanto faz se a categoria está em uso ou não
Pode ser enviado um parametro "substitute" para substituir a categoria por outra
"""


@login_required
def remove_category(request):
    args = '{}'
    if request.method != 'POST':
        return {"code": 400, "response": "Categoria não encontrada"}
    
    category_id = request.GET.get('id')
    substitute = request.GET.get('substitute')
    if category_id:
        category = Category.objects.filter(id=category_id).first()
        if category:
            if substitute:
                questions = Question.objects.filter(category_id=category_id)
                for question in questions:
                    question.category_id = substitute
                    question.save()
            category.delete()   
            args = {"code": 200, "response": "Categoria removida com sucesso"}
        else:
            args = {"code": 404, "response": "Categoria não encontrada"}
    else:
        args = {"code": 400, "response": "Categoria não encontrada"}
    return args