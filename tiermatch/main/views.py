import json
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import *

from .reponse import response

@login_required
def index(request):
    return render(request, 'pages/home.html', {})

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
        args = {"code": 403, "response": "Ação inválida"}
            
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
        args = {"code": 403, "response": "Ação inválida"}
            
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
        args = {"code": 403, "response": "Ação inválida"}
    return args

@login_required
def create_category(request):
    args = {'method': 'criar', 'suffix': 'categoria', 'route': 'category/create'}
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        color = data.get('color')
        if name and color:
            category = Category(name=name, color=color)
            category.save()
            return response(200, args)
        else:
            return response(400, args)
    else:
        return response(403, args)
    
@login_required
def remove_category(request):
    args = '{}'
    if request.method != 'POST':
        return {"code": 403, "response": "Ação inválida"}
    
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

"""
ROTA / GET / QUESTIONS
Rota de busca de questões
É necessário passar o quiz_id que a questão pertence
"""
def get_question(request):
    if request.method != 'GET':
        return {"code": 403, "response": "Ação inválida"}
    quiz_id = request.GET.get('quiz_id')
    args = '{}'
    if quiz_id:
        questions = Question.objects.filter(quiz_id=quiz_id)
        if questions:
            args = {"code": 200, "response": questions}
        else:
            args = {"code": 404, "response": "Questões não encontradas"}
    else:
        args = {"code": 400, "response": "Questões não encontradas"}
    return args

"""
ROTA / DELETE / QUESTION
Rota de remoção de questões
É necessário passar o id da questão
"""


def delete_question(request):
    if request.method != 'POST':
        return {"code": 403, "response": "Ação inválida"}
    question_id = request.POST.get('id')
    args = '{}'
    if question_id:
        question = Question.objects.filter(id=question_id).first()
        quiz_original = Quiz.objects.filter(id=question.quiz_id).first()
        if quiz_original.user_id == request.user.id:
            question.delete()
            args = {"code": 200, "response": "Questão removida com sucesso"}
        else:
            args = {"code": 403, "response": "Você não tem permissão para remover essa questão"}
    else:
        args = {"code": 400, "response": "Questão não encontrada"}

    return args


def set_question(request):
    if request.method != 'POST':
        return {"code": 403, "response": "Ação inválida"}
    data = request.POST.get('data')
    args = '{}'
    if data.id:
        quiz = Quiz.objects.filter(id=data['quiz_id']).first()
        if quiz.user_id == request.user.id:
            question = Question(
                name=data['name'],
                image=data['image'],
                attribute=data['attribute'],
                quiz_id=data['quiz_id'],
            )
            question.save()
            args = {"code": 200, "response": question}
        else:
            args = {"code": 403, "response": "Você não tem permissão para adicionar questões nesse quiz"}
    else:
        args = {"code": 400, "response": "Quiz não encontrado"}
    return args


def get_answer(request):
    if request.method != 'GET':
        return {"code": 403, "response": "Ação inválida"}
    question_id = request.GET.get('question_id')
    args = '{}'
    if question_id:
        answers = Answer.objects.filter(question_id=question_id)
        if answers:
            args = {"code": 200, "response": answers}
        else:
            args = {"code": 404, "response": "Respostas não encontradas"}
    else:
        args = {"code": 400, "response": "Respostas não encontradas"}
    return args


def set_answer(request):
    if request.method != 'POST':
        return {"code": 403, "response": "Ação inválida"}
    data = request.POST.get('data')
    args = '{}'
    if data:
        if data['answers'] and data['answer']:
            quiz = Quiz.objects.filter(id=data['answer']).first()
            if quiz:
                respost = Answers(id_user=request.user.id, id_quiz=quiz.id)
                respost.save()
                for answer in data['answers']:
                    answer = Answer(
                        id_question=answer['id_question'],                        
                        id_answer=answer['id_answer'],
                        value=answer['value'],
                    )
                    answer.save()
                args = {"code": 200, "response": "Respostas salvas com sucesso"}
            else:
                args = {"code": 404, "response": "Quiz não encontrado"}
        else:
            args = {"code": 400, "response": "Respostas não encontradas"}
    return args