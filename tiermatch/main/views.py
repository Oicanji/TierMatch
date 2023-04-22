import json
from django.shortcuts import render
from datetime import datetime
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
def get_quiz(request):
    args = {'method': 'buscar', 'suffix': 'quiz', 'route': 'quiz/get'}
    if request.method != 'GET':
        return response(403, args)
    data = json.loads(request.body)
    if data.get('id'):
        quiz = Quiz.objects.filter(id=data.get('id')).first()
        if quiz:
            args['response'] = [quiz]
            return response(200, args)
        else:
            return response(404, args)
    else:
        return response(400, args)

@login_required
def get_popular_quizzes(request):
    args = {'method': 'buscar', 'suffix': 'quiz', 'route': 'quizzes/popular'}
    if request.method != 'GET':
        return response(403, args)
    most_answers = Answer.objects.values('quiz_id').annotate(total=Count('quiz_id')).order_by('-total')
    quizzes_with_most_answers = []
    for answer in most_answers:
        quiz = Quiz.objects.filter(id=answer['quiz_id']).first()
        if quiz:
            quizzes_with_most_answers.append(quiz)
    if quizzes_with_most_answers:
        args['response'] = quizzes_with_most_answers
        return response(200, args)
    else:
        args['response'] = []
        return response(404, args)

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

# @login_required
# def get_quizzes(request):
#     args = {'method': 'buscar', 'suffix': 'quiz', 'route': 'quiz/get'}
#     if request.method != 'GET':
#         return response(403, args)
#     data = json.loads(request.body)
#     for key in data:
#         if key not in ['like', 'category', 'user', 'offset', 'limit', 'id']:
#             return response(400, args)




"""
ROTA / SET / QUIZ
Rota de criação do quiz
Tem que ser passados os seguintes parametros:
name = nome do quiz
description = descrição do quiz
create_by = id do usuário que está criando o quiz

super_allow_allias = alias do super_allow
allow_allias = alias do allow
deny_allias = alias do deny

super_allow_color = cor do super_allow
allow_color = cor do allow
deny_color = cor do deny
"""

@login_required
def set_quiz(request):
    args = {'method': 'criar', 'suffix': 'quiz', 'route': 'quiz/set'}
    if request.method != 'POST':
        return response(403, args)
    current_user = request.user.id
    print(current_user)
    data = json.loads(request.body)
    if not data:
        return response(400, args)
    if not data.get('name') or not data.get('description') or not data.get('super_allow_allias') or not data.get('allow_allias') or not data.get('deny_allias') or not data.get('super_allow_color') or not data.get('allow_color') or not data.get('deny_color'):
        return response(400, args)
    res = []
    params = {
        "name": data.get('name'),
        "description": data.get('description'),   
        "create_by_id":  current_user,
        "create_at": datetime.now(),
        "super_allow_allias": data.get('super_allow_allias'),
        "allow_allias": data.get('allow_allias'),
        "deny_allias": data.get('deny_allias'),
        "super_allow_color": data.get('super_allow_color'),
        "allow_color": data.get('allow_color'),
        "deny_color": data.get('deny_color'),
    }
    quiz = Quiz(name=params.get('name'), description=params.get('description'), create_by_id=params.get('create_by_id'), create_at=params.get('create_at'),
                super_allow_allias=params.get('super_allow_allias'), allow_allias=params.get('allow_allias'), deny_allias=params.get('deny_allias'),
                super_allow_color=params.get('super_allow_color'), allow_color=params.get('allow_color'), deny_color=params.get('deny_color'))

    quiz.save()
    quiz = Quiz.objects.filter(id=quiz.id).first()
    res.append({"name": quiz.name, "description": quiz.description, "create_by_id": quiz.create_by_id, "create_at": quiz.create_at, 
                    "super_allow_allias": quiz.super_allow_allias, "allow_allias": quiz.allow_allias, "deny_allias": quiz.deny_allias, 
                        "super_allow_color": quiz.super_allow_color, "allow_color": quiz.allow_color, "deny_color": quiz.deny_color})
    args['response'] = res
    return response(200, args)

"""
ROTA / EDIT / QUIZ
Rota de cadastro da edição do quiz
Apenas o usuário que criou o quiz pode editar
Todos os parametros são opcionais, mas pelo menos um tem que ser passado, o id do quiz
"""

@login_required
def edit_quiz(request):
    args = {'method': 'editar', 'suffix': 'quiz', 'route': 'quiz/edit'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    if not data:
        return response(400, args)
    quiz = Quiz.objects.filter(id=data.get('id')).first()
    res = []
    if quiz:
        for key in data:
            if key not in ['name', 'description', 'super_allow_allias', 'allow_allias', 'deny_allias', 'super_allow_color', 'allow_color', 'deny_color']:
                return response(400, args)
        for key in data:
            if key in ['name', 'description', 'super_allow_allias', 'allow_allias', 'deny_allias', 'super_allow_color', 'allow_color', 'deny_color']:
                setattr(quiz, key, data.get(key))
        quiz.save()
        quiz = Quiz.objects.filter(id=quiz.id).first()
        res.append({"name": quiz.name, "description": quiz.description, "super_allow_allias": quiz.super_allow_allias, "allow_allias": quiz.allow_allias, 
                    "deny_allias": quiz.deny_allias, "super_allow_color": quiz.super_allow_color, 
                    "allow_color": quiz.allow_color, "deny_color": quiz.deny_color})
        args['response'] = res
        return response(200, args)
    else:
        return response(404, args)


"""
ROTA / REMOVE / QUIZ
Rota de remoção do quiz
Apenas o usuário que criou o quiz pode remove-lo
"""

def remove_quiz(request):
    args = {'method': 'remover', 'suffix': 'quiz', 'route': 'quiz/remove'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    if not data:
        return response(400, args)
    quiz = Quiz.objects.filter(id=data.get('id')).first()
    if not quiz:
        return response(404, args) 
    current_user = request.user.id
    if current_user != quiz.create_by_id:
        return response(403, args)
    quiz.delete()
    return response(200, args)
    
"""
create a routes get, set and remove for category 
"""
@login_required
def get_category(request):
    args = {'method': 'buscar', 'suffix': 'categoria', 'route': 'category/get'}
    data = {}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)

    res = []
    if data.get('categories'):
        ids = data.get('categories')
        for id in ids:
            category = Category.objects.filter(id=id).first()
            if category:
                res.append({'id': category.id, 'name': category.name, 'color': category.color})
    else:
        category = Category.objects.all()
        for cat in category:
            res.append({'id': cat.id, 'name': cat.name, 'color': cat.color})
    args['response'] = res
    return response(200, args)

@login_required
def create_category(request):
    args = {'method': 'criar', 'suffix': 'categoria', 'route': 'category/create'}
    if request.method != 'POST':
        return response(403, args)

    data = json.loads(request.body)
    name = data.get('name')
    color = data.get('color')
    if name and color:
        category = Category(name=name, color=color)
        category.save()
        return response(200, args)
    else:
        return response(400, args)


# LEMBRAR DE FAZER O PARAMETRO SUBSTITUTE
@login_required
def remove_category(request):
    args = {'method': 'remover', 'suffix': 'categoria', 'route': 'category/remove'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    if data.get('id'):
        category = Category.objects.filter(id=data.get('id')).first()
        if category:
            category.delete()
            return response(200, args)
        else:
            return response(404, args)
    else:
        return response(400, args)

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