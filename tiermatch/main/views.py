from collections import Counter
import json
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import *

from .reponse import response, format_values, format_values_question

@login_required
def index(request):
    quizzes = Quiz.objects.all()
    res = []
    for quiz in quizzes:
        quiz_dict = {
            "id": quiz.id,
            "name": quiz.name,
            "description": quiz.description,
            "create_at": quiz.create_at.strftime("%d/%m/%Y %H:%M:%S"),
            "super_allow_allias": quiz.super_allow_allias,
            "allow_allias": quiz.allow_allias,
            "deny_allias": quiz.deny_allias,
            "super_allow_color": quiz.super_allow_color,
            "allow_color": quiz.allow_color,
            "deny_color": quiz.deny_color,
        }
        if quiz.create_by == request.user:
            quiz_dict['is_owner'] = True
        else:
            quiz_dict['is_owner'] = False
        categories = Categories.objects.filter(quiz_id=quiz.id)
        list_categories = []
        for category in categories:
            cat = Category.objects.filter(id=category.categories_id.id).first()
            list_categories.append({'id': cat.id, 'name': cat.name, 'color': cat.color})
        quiz_dict['categories'] = list_categories

        image_question = ''
        questions = Question.objects.filter(quiz_id=quiz.id)
        for question in questions:
            image_question = question.image
            break
        if image_question != '':
            quiz_dict['image'] = image_question
        else:
            quiz_dict['image'] = ('static/images/not_found.png')

        res.append(quiz_dict)

    res =json.dumps(res)
    #get categories with quiz_id = quiz.id
    return render(request, 'pages/home.html', {"res": res})


def undefined(request):
    return render(request, 'pages/undefined.html', {})

@login_required
def my_quizzes(request):
    return render(request, 'pages/my_quizzes.html', {})

@login_required
def create_quiz(request, quiz_id=None):
    if quiz_id is not None:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz:
            res = {
                "id": quiz.id,
                "name": quiz.name,
                "description": quiz.description,
                "create_at": quiz.create_at.strftime("%d/%m/%Y %H:%M:%S"),
                "super_allow_allias": quiz.super_allow_allias,
                "allow_allias": quiz.allow_allias,
                "deny_allias": quiz.deny_allias,
                "super_allow_color": quiz.super_allow_color,
                "allow_color": quiz.allow_color,
                "deny_color": quiz.deny_color,
            }
            list_categories_saves = []
            category_exists = Categories.objects.filter(quiz_id=quiz.id)
            for category in category_exists:
                list_categories_saves.append(category.categories_id.id)

            res['categories'] = list_categories_saves
            a = json.dumps(res)
         
            context = {
                "res": a,
            }
            return render(request, 'pages/create_quiz.html', context)
            
    return render(request, 'pages/create_quiz.html', {"res": {}})



@login_required
def play(request, id_url):
    if request.method != 'GET' or id_url is None:
        return render(request, "pages/undefined.html")
    
    quiz = Quiz.objects.filter(id=id_url).first()
    if quiz:
        context = {}
        res = {
            "id": quiz.id,
            "name": quiz.name,
            "description": quiz.description,
            "create_by_id": quiz.create_by.username,
            "date": quiz.create_at.strftime("%d/%m/%Y %H:%M:%S"),
            "super_allow_alias": quiz.super_allow_allias,
            "allow_alias": quiz.allow_allias,
            "deny_alias": quiz.deny_allias,
            "super_allow_color": quiz.super_allow_color,
            "allow_color": quiz.allow_color,
            "deny_color": quiz.deny_color,
            "categories": [],
            "questions": [],
        }
        categories = Categories.objects.filter(quiz_id=quiz)
        for category in categories:
            cat = Category.objects.filter(id=category.categories_id.id).first()
            res['categories'].append({
                "id": cat.id,
                "name": cat.name,
                "color": cat.color
            })
            
        questions = Question.objects.filter(quiz_id=quiz.id)
        for question in questions:
            res['questions'].append({
                "id": question.id,
                "name": question.name,
                "image": question.image,
                "stats": question.attribute.replace("'", '"'),
            })
        res = json.dumps(res)
        context['quiz'] = res
        return render(request, 'pages/play.html', context)
    return render(request, 'pages/undefined.html', {})


@login_required
def results(request):
    return render(request, 'pages/results.html', {})

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
            list_categories = data.get('categories')
            list_categories_saves = []
            if list_categories is not None and len(list_categories) > 0:
                for category in list_categories:
                    category_exists = Category.objects.filter(id=category).first()
                    if category_exists:
                        category = Categories(quiz_id=quiz, categories_id=category_exists)
                        list_categories_saves.append({"quiz_id": category.quiz_id.id, "categories_id": category.categories_id.id})
            res = []
            res.append({"name": quiz.name, "description": quiz.description, "create_by_id": quiz.create_by_id, "create_at": quiz.create_at, 
                            "super_allow_allias": quiz.super_allow_allias, "allow_allias": quiz.allow_allias, "deny_allias": quiz.deny_allias, 
                                "super_allow_color": quiz.super_allow_color, "allow_color": quiz.allow_color, 
                                    "deny_color": quiz.deny_color, "categories": list_categories_saves})
            args['response'] = res
            args['response'] = format_values(args)
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
    most_answers = Answer.objects.values('quiz_id').annotate(total=Counter('quiz_id')).order_by('-total')
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

@login_required
def set_quiz(request):
    args = {'method': 'criar', 'suffix': 'quiz', 'route': 'quiz/set'}
    if request.method != 'POST':
        return response(403, args)
    current_user = request.user.id
    data = json.loads(request.body)
    if not data:
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

    list_categories = data.get('categories')
    list_categories_saves = []
    if list_categories is not None and len(list_categories) > 0:
        for category in list_categories:
            category_exists = Category.objects.filter(id=category).first()
            if category_exists:
                category = Categories(quiz_id=quiz, categories_id=category_exists)
                category.save()

                list_categories_saves.append({"quiz_id": category.quiz_id.id, "categories_id": category.categories_id.id})

    res.append({
        "id": quiz.id,
        "name": quiz.name, "description": quiz.description, 
        "create_by_id": quiz.create_by, "create_at": quiz.create_at, 
        "super_allow_allias": quiz.super_allow_allias, "allow_allias": quiz.allow_allias, 
        "deny_allias": quiz.deny_allias, "super_allow_color": quiz.super_allow_color, 
        "allow_color": quiz.allow_color, "deny_color": quiz.deny_color,
        "categories": list_categories_saves
    })
    
    args['response'] = res
    args['response'] = format_values(args)
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
    if request.user.id != quiz.create_by.id:
        return response(403, args)
    res = []
    if quiz:
        for key in data:
            if key not in ['id', 'name', 'description', 'super_allow_allias', 'allow_allias', 'deny_allias', 'super_allow_color', 'allow_color', 'deny_color', 'categories']:
                return response(400, args)

        quiz.name = data.get('name')
        quiz.description = data.get('description')
        quiz.super_allow_allias = data.get('super_allow_allias')
        quiz.allow_allias = data.get('allow_allias')
        quiz.deny_allias = data.get('deny_allias')
        quiz.super_allow_color = data.get('super_allow_color')
        quiz.allow_color = data.get('allow_color')
        quiz.deny_color = data.get('deny_color')
        quiz.save()

        list_categories = data.get('categories')
        list_categories_saves = []
        if list_categories is not None and len(list_categories) > 0:
            for category in list_categories:
                category_exists = Category.objects.filter(id=category).first()
                if category_exists:
                    category = Categories(quiz_id=quiz, categories_id=category_exists)
                    category.save()
                    list_categories_saves.append({"quiz_id": category.quiz_id.id, "categories_id": category.categories_id.id})
        res.append({
            "id": quiz.id,
            "name": quiz.name, "description": quiz.description, 
            "create_by_id": quiz.create_by, "create_at": quiz.create_at, 
            "super_allow_allias": quiz.super_allow_allias, "allow_allias": quiz.allow_allias, 
            "deny_allias": quiz.deny_allias, "super_allow_color": quiz.super_allow_color, 
            "allow_color": quiz.allow_color, "deny_color": quiz.deny_color,
            "categories": list_categories_saves
        })
                
        args['response'] = res
        args['response'] = format_values(args)
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
    print(data)
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


@login_required
def create_question(request):
    args = {'method': 'criar', 'suffix': 'pergunta', 'route': 'question/create'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    name = data.get('name')
    image = data.get('image')
    attribute = data.get('attribute')
    quiz_id = data.get('quiz_id')
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz.create_by_id != request.user.id:
        return response(403, args)
    if name and image and attribute and quiz_id:
        question = Question(name=name, image=image, attribute=attribute, quiz_id=quiz)
        question.save()
        question = Question.objects.filter(id=question.id).first()
        res = []
        res.append({"id": question.id, "name": question.name, "image": question.image, "attribute": question.attribute, "quiz_id": question.quiz_id.id})
        args['response'] = res
        args['response'] = format_values_question(args)
        return response(200, args)
    else:
        return response(400, args)


@login_required
def get_question_all(request):
    args = {'method': 'buscar todos', 'suffix': 'pergunta', 'route': 'question/get/all'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    id = data.get('id')
    question = Question.objects.filter(quiz_id=id)
    res = []
    for q in question:
        question_dict = {
            "id": q.id, 
            "name": q.name, 
            "attribute": q.attribute, 
            "image": q.image,
            "quiz_id": q.quiz_id.id
            }
        res.append(question_dict)
    args['response'] = res
    res['response'] = format_values_question(args)
    return response(200, args)

@login_required
def get_question_id(request):
    args = {'method': 'buscar por id', 'suffix': 'pergunta', 'route': 'question/get/id'}
    data = json.loads(request.body)
    if request.method != 'GET':
        return response(403, args)
    res = []
    if data.get('id'):
        question = Question.objects.filter(id=data.get('id')).first()
        res.append({"id": question.id, "name": question.name, 
                    "image": question.image, "attribute": question.attribute, "quiz_id": question.quiz_id})
        args['response'] = res
        return response(200, args)



@login_required
def edit_question(request):
    args = {'method': 'editar', 'suffix': 'pergunta', 'route': 'question/edit'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    if not data:
        return response(400, args)
    question = Question.objects.filter(id=data.get('id')).first()
    res = []
    if question:
        for key in data:
            if key not in ['name', 'description', 'image', 'attribute', 'quiz_id']:
                return response(400, args)
        for key in data:
            if key in ['name', 'description', 'image', 'attribute', 'quiz_id']:
                setattr(question, key, data.get(key))
        question.save()
        question = Question.objects.filter(id=question.id).first()
        res.append({"name": question.name, "description": question.description, "image": question.image, "attribute": question.attribute, "quiz_id": question.quiz_id})
        args['response'] = res
        res['response'] = format_values(args)
        return response(200, args)
    else:
        return response(404, args)


@login_required
def remove_question(request):
    args = {'method': 'remover', 'suffix': 'pergunta', 'route': 'question/remove'}
    if request.method != 'POST':
        return response(403, args)
    data = json.loads(request.body)
    if not data:
        return response(400, args)
    question = Question.objects.filter(id=data.get('id')).first()
    if not question:
        return response(404, args)
    question.delete()
    return response(200, args)
