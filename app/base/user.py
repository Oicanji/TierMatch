from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db

class User:

    @classmethod
    def _validate_user_exists(cls, request: dict):
        email = request.form.get('email')
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            return flash('Email já existe.', category='error')
        return cls._create_user(request)

    @classmethod
    def _create_user(cls, request: dict):
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            return flash('Email deve ter mais de 3 caracteres.', category='error')
        elif len(first_name) < 2:
            return flash('O nome deve ter mais de 1 caracter.', category='error')
        elif password1 != password2:
            return flash('Senhas não conferem.', category='error')
        elif len(password1) < 7:
            return flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1,
                                                            method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return True
    
    @classmethod
    def _validate_user_login(cls, request: dict):
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return True
            else:
                return flash('Senha incorreta.', category='error')
        else:
            return flash('Email não existe.', category='error')