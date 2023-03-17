from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user
from flask import request, jsonify

from .models import *
from .param_return import *

response = paramReturm()

views = Blueprint('views', __name__)

"""
ROTA / HOME
Quando o usuário acessar a página inicial, verificar se ele está logado
Se estiver logado, enviar o objeto do usuário para a página inicial
"""
@views.route('/')
def home():
    user = current_user
    return render_template("pages/home.html", user=user)

"""
ROTA / CADASTRAR
Quando o usuário acessar a página de cadastro dos quiz
Um usuário não pode entrar se não estiver logado
Um usuário só pode editar os quiz que ele criou
Caso o usuário não tenha passado o id do quiz, ele vai criar um novo quiz e não vai editar
"""
@views.route('/cadastrar', methods=['GET'])
def cadastrar_quiz():
    user = current_user
    if not user.is_authenticated:
        return render_template("pages/acesso_proibido.html")

    id = request.args.get('id')
    args = '{}'
    if id:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            if quiz.user_id == current_user.id:
                args = response.parse(200, {"action": "edit", "quiz": quiz})
            else:
                args = response.parse(403, {"action": "create", "quiz": "{}"})
        else:
            args = response.parse(404, {"action": "create", "quiz": "{}"})
    else:
        args = response.parse(200, {"action": "create", "quiz": "{}"})
            
    return render_template("pages/cadastrar_quiz.html", args=args)

"""
ROTA / PLAY
Rota que o usuário vai acessar para jogar o quiz
Tem que ser enviado o id do quiz caso contrário, envie para o acesso proibido
"""
@views.route('/play', methods=['GET'])
def play_quiz():
    id = request.args.get('id')
    if id:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            return render_template("pages/fazer_quiz.html", quiz=quiz)
        else:
            return render_template("pages/acesso_proibido.html")
    else:
        return render_template("pages/acesso_proibido.html")

"""
ROTA / GET / QUIZ
Quando o usuário quer buscar um quiz dentro do banco
Ele vai passar o id do quiz e vai retornar o quiz
"""
@views.route('/get/quiz/', methods=['GET'])
def get_quiz(id):
    id = request.args.get('id')
    if id:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            return response.parse(200, {"quiz": quiz})
        else:
            return response.parse(404, {"quiz": "{}"})
    else:
        return response.parse(400, {"quiz": "{}"})

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
@views.route('/get/quizzes/', methods=['GET'])
def get_quizzes():
    like = request.args.get('like')
    category = request.args.get('category')
    user = request.args.get('user')
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    order_by = request.args.get('order_by')
    
    if not by:
        by = 0
    if not limit:
        limit = 50

    #varivel que vai guardar os filtros
    filters = []

    #verificar se tem o filtro like
    if like:
        filters.append(Quiz.name.like('%' + like + '%'))

    #verificar se tem o filtro category
    if category:
        filters.append(Quiz.category == category)

    #verificar se tem o filtro user
    if user:
        filters.append(Quiz.user_id == user)

    #verificar se tem o filtro order_by
    if order_by == 'desc':
        order_by = Quiz.id.desc()
    elif order_by == 'asc':
        order_by = Quiz.id.asc()
    else:
        order_by = Quiz.id.desc()
        
    quizzes = Quiz.query.filter(*filters).order_by(order_by).offset(offset).limit(limit).all()
    if quizzes:
        return response.parse(200, {"quizzes": quizzes})
    else:
        return response.parse(404, {"quizzes": "{}"})

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
@views.route('/set/quiz', methods=['POST'])
def set_quiz():
    if not current_user.is_authenticated:
        return response.parse(403)

    data = request.get_json()
    if data:
        if data['name'] and data['description'] and data['create_by'] and data['super_allow_alias'] and data['allow_alias'] and data['deny_alias'] and data['super_allow_color'] and data['allow_color'] and data['deny_color']:
            if data['create_by'] == current_user.id:
                quiz = Quiz(name=data['name'], description=data['description'], create_by=data['create_by'], super_allow_alias=data['super_allow_alias'], allow_alias=data['allow_alias'], deny_alias=data['deny_alias'], super_allow_color=data['super_allow_color'], allow_color=data['allow_color'], deny_color=data['deny_color'])
                db.session.add(quiz)
                db.session.commit()

                #eu nao sei fazer isso direito, mas eu to tentando
                quiz = Quiz.query.filter_by(name=data['name'], description=data['description'], create_by=data['create_by'], super_allow_alias=data['super_allow_alias'], allow_alias=data['allow_alias'], deny_alias=data['deny_alias'], super_allow_color=data['super_allow_color'], allow_color=data['allow_color'], deny_color=data['deny_color']).first()
                #socorro

                return response.parse(200, {"quiz": quiz})
            else:
                return response.parse(403)
        else:
            return response.parse(400)
    else:
        return response.parse(400)

"""
ROTA / EDIT / QUIZ
Rota de cadastro da edição do quiz
Apenas o usuário que criou o quiz pode editar
Todos os parametros são opcionais, mas pelo menos um tem que ser passado, o id do quiz
"""
@views.route('/edit/quiz', methods=['POST'])
def edit_quiz():
    if not current_user.is_authenticated:
        return response.parse(403)

    data = request.get_json()
    if data:
        if data['id']:
            quiz = Quiz.query.filter_by(id=data['id']).first()
            if quiz:
                if quiz.create_by == current_user.id:
                    if data['name']:
                        quiz.name = data['name']
                    if data['description']:
                        quiz.description = data['description']
                    if data['super_allow_alias']:
                        quiz.super_allow_alias = data['super_allow_alias']
                    if data['allow_alias']:
                        quiz.allow_alias = data['allow_alias']
                    if data['deny_alias']:
                        quiz.deny_alias = data['deny_alias']
                    if data['super_allow_color']:
                        quiz.super_allow_color = data['super_allow_color']
                    if data['allow_color']:
                        quiz.allow_color = data['allow_color']
                    if data['deny_color']:
                        quiz.deny_color = data['deny_color']
                    db.session.commit()
                    return response.parse(200, {"quiz": quiz})
                else:
                    return response.parse(403, {"quiz": "{}"})
            else:
                return response.parse(404, {"quiz": "{}"})
        else:
            return response.parse(400, {"quiz": "{}"})
    else:
        return response.parse(400, {"quiz": "{}"})

"""
ROTA / GET / CATEGORY
Rota de busca de uma categoria apenas
Tem que ser passado o id da categoria
"""
@views.route('/get/category', methods=['GET'])
def get_category():
    if not current_user.is_authenticated:
        return response.parse(403)

    id = request.args.get('id')
    if id:
        category = Category.query.filter_by(id=id).first()
        if category:
            return response.parse(200, {"category": category})
    return response.parse(404)

"""
ROTA / GET / CATEGORIES
Rota de busca de categorias
Tem que ser passado os id "offset" e "limit" para a paginação funcionar
A busca deve ser feita de forma crescente
"""
@views.route('/get/categories', methods=['GET'])
def get_categories():
    if not current_user.is_authenticated:
        return response.parse(403)

    offset = request.args.get('offset')
    if not offset:
        offset = 0
    limit = request.args.get('limit')
    if not limit:
        limit = 25

    if offset and limit:
        categories = Category.query.offset(offset).limit(limit).all()

    if categories:
        return response.parse(200, {"categories": categories})
    return response.parse(404)

"""
ROTA / SET / CATEGORY
Rota de cadastro de uma categoria
"""
@views.route('/set/category', methods=['POST'])
def set_category():
    if not current_user.is_authenticated:
        return response.parse(403)

    data = request.get_json()
    if data:
        if data['name'] and data['color']:
            category = Category(name=data['name'], color=data['color'])
            db.session.add(category)
            db.session.commit()
            return response.parse(200, {"category": category})
        else:
            return response.parse(400)
    else:
        return response.parse(400)


"""
ROTA / REMOVE / CATEGORY
Sim não é necessário editar uma categoria, apenas remover e criar uma nova
Tem que ser passado o id da categoria
Tanto faz se a categoria está em uso ou não
Pode ser enviado um parametro "substitute" para substituir a categoria por outra
"""
@views.route('/remove/category', methods=['POST'])
def remove_category():
    if not current_user.is_authenticated:
        return response.parse(403)

    id = request.args.get('id')
    substitute = request.args.get('substitute')
    if id:
        category = Category.query.filter_by(id=id).first()
        if category:
            if substitute:
                substitute = Category.query.filter_by(id=substitute).first()
                if substitute:
                    questions = Question.query.filter_by(category=category.id).all()
                    for question in questions:
                        question.category = substitute.id
                        db.session.commit()
                else:
                    return response.parse(404)
            db.session.delete(category)
            db.session.commit()
            return response.parse(200)
        else:
            return response.parse(404)
    return response.parse(400)

"""
ROTA / GET / QUESTIONS
Rota de busca de questões
É necessário passar o quiz_id que a questão pertence
"""
@views.route('/get/question', methods=['GET'])
def get_question():
    quiz_id = request.args.get('quiz_id')
    if quiz_id:
        question = Question.query.filter_by(quiz=quiz_id).first()
        if question:
            return response.parse(200, {"question": question})
        else:
            return response.parse(404)
    else:
        return response.parse(400)
        
"""
ROTA / DELETE / QUESTION
Rota de remoção de questões
É necessário passar o id da questão
"""
@views.route('/delete/question', methods=['POST'])
def delete_question():
    if not current_user.is_authenticated:
        return response.parse(403)
    id = request.args.get('id')
    if id:
        quiz_by = Quiz.query.filter_by(id=Question.query.filter_by(id=id).first().quiz).first().create_by
        if quiz_by == current_user.id:
            question = Question.query.filter_by(id=id).first()
            if question:
                db.session.delete(question)
                db.session.commit()
                return response.parse(200)
            else:
                return response.parse(404)
        else:
            return response.parse(403)
    else:
        return response.parse(400)
    
"""
ROTA / GET / ANSWERS
Rota de busca de respostas
É necessário passar o question_id e o 
"""
@views.route('/set/answers', methods=['POST'])
def set_answers():
    data = request.get_json()
    if data:
        for answer in data['response']:
            if answer['id'] and answer['answer']:
                answer = Answer.query.filter_by(id=answer['id']).first()
                if answer:
                    answer.answer = answer['answer']
                    db.session.commit()
    
    return jsonify({'code': 200, 'message': 'Respostas cadastradas com sucesso'})

# '/set/category_to_quiz'
# Vou te mandar um parâmetro 'category_id' e um 'quiz_id' e faz o teu, só lembra de ver que a sessão pode assinar naquele quiz.
@views.route('/set/category_to_quiz', methods=['POST'])
def set_category_to_quiz():
    category_id = request.args.get('category_id')
    quiz_id = request.args.get('quiz_id')
    if category_id and quiz_id:
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz:
            if quiz.user_id == current_user.id:
                quiz.category_id = category_id
                db.session.commit()
                return jsonify({'code': 200, 'message': 'Categoria adicionada com sucesso'})
            else:
                return jsonify({'code': 403, 'message': 'Acesso negado'})
        else:
            return jsonify({'code': 404, 'message': 'Quiz não encontrado'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})


# '/set/question'
# Vou te mandar um json da seguinte forma:
# data {
#   name
#   image: "vai ter a url aqui"
#   quiz_id
#   atributes "negocio que eu esqueci, deixa isso só no front mesmo, eu me viro"
# }
# Só lembra da parada de ver se a sessão pode apontar para esse quiz.
@views.route('/set/question', methods=['POST'])
def set_question():
    data = request.get_json()
    if data:
        if data['quiz_id']:
            quiz = Quiz.query.filter_by(id=data['quiz_id']).first()
            if quiz:
                if quiz.user_id == current_user.id:
                    question = Question(name=data['name'], image=data['image'], quiz_id=data['quiz_id'], atributes=data['atributes'])
                    db.session.add(question)
                    db.session.commit()
                    return jsonify({'code': 200, 'message': 'Questão adicionada com sucesso'})
                else:
                    return jsonify({'code': 403, 'message': 'Acesso negado'})
            else:
                return jsonify({'code': 404, 'message': 'Quiz não encontrado'})
        else:
            return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})

@views.route('/remove/question', methods=['POST'])
def remove_question():
    id = request.args.get('id')
    if id:
        question = Question.query.filter_by(id=id).first()
        if question:
            if question.quiz.user_id == current_user.id:
                db.session.delete(question)
                db.session.commit()
                return jsonify({'code': 200, 'message': 'Questão removida com sucesso'})
            else:
                return jsonify({'code': 403, 'message': 'Acesso negado'})
        else:
            return jsonify({'code': 404, 'message': 'Questão não encontrada'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})

@views.route('/edit/question', methods=['POST'])
def edit_question():
    data = request.get_json()
    if data:
        if data['id']:
            question = Question.query.filter_by(id=data['id']).first()
            if question:
                if question.quiz.user_id == current_user.id:
                    question.name = data['name']
                    question.image = data['image']
                    question.atributes = data['atributes']
                    db.session.commit()
                    return jsonify({'code': 200, 'message': 'Questão editada com sucesso'})
                else:
                    return jsonify({'code': 403, 'message': 'Acesso negado'})
            else:
                return jsonify({'code': 404, 'message': 'Questão não encontrada'})
        else:
            return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})
# '/get/anwsers'
# Te passo 'id"
# Quiero:
# data: { results = [...] }
# JSON favorcito
# Y...
# Vê se não precisa ver o o quiz é do usuário pois qualquer usuário pode fazer um quiz.
@views.route('/get/answers', methods=['GET'])
def get_answers():
    id = request.args.get('id')
    if id:
        answers = Answer.query.filter_by(question_id=id).all()
        if answers:
            return jsonify({'code': 200, 'message': 'Respostas encontradas', 'results': answers})
        else:
            return jsonify({'code': 404, 'message': 'Nenhuma resposta encontrada', 'results': {}})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos', 'results': {}})