from .db import db
from flask_login import UserMixin
from .base.user import User as UserEntity

"""
QUIZ - Questionários
Classe de questionários
É responsável por armazenar os questionários criados pelos usuários
Possuem uma lista de perguntas (Question) e uma lista de categorias (ListCategories)
Ou seja
Um questionário possui várias perguntas e várias categorias

Ele também no parametro 'create_by' que é uma relação com a tabela de usuários (User)
"""
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    create_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    allow_allias = db.Column(db.String(100))
    super_allow_allias = db.Column(db.String(100))
    deny_allias = db.Column(db.String(100))
    allow_color = db.Column(db.String(7))
    deny_color = db.Column(db.String(7))
    allow_color_super = db.Column(db.String(7))
    list_answers = db.relationship('Answers')
    list_categories = db.relationship('ListCategories')

"""
LIST QUESTIONS - Perguntas
Perguntas cadastras nos questionário
A classe attribute possui um JSON para ser intepretada por uma biblioteca de atributos
No atributo 'image' é armazenado o caminho da imagem
Possuem uma relação com a tabela de questionários (Quiz)
"""
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(500))
    attribute = db.Column(db.String(20000))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

"""
LIST CATEGORIES - Lista de categorias
É responsável por armazenar uma lista de categorias de cada questionário
Possuem uma relação com a tabela de questionários (Quiz)
Possuem uma relação com a tabela de categorias (Category)
"""
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

"""
CATEGORIES - Categorias
É responsável os dados de uma categoria
O valor do 'color' é um código hexadecimal
"""
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))


"""
ANSWERS - Resolução dos questionários
"""
class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    list_answers = db.relationship('Answer')

"""
ANSWER - Respostas dos questionários
É responsável por armazenar as respostas dos usuários
O valor é normalmente 'deny' ou 'allow' ou 'super_allow'
"""
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
    value = db.Column(db.String(100))
    id_answers = db.Column(db.Integer, db.ForeignKey('answers.id'))

"""
USER - Usuários
Classe dos usuários do sistema
"""
class User(db.Model, UserMixin, UserEntity):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    type = db.Column(db.String(100))
