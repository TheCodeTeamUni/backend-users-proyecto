import uuid
from flask_restful import Resource
from flask import request
from ..models import db, User, UserSchema
from ..utils import encrypt

user_schema = UserSchema()


class ViewUsers(Resource):

    def get(self):
        # Retorna todos los usuarios registrados: /users/all
        return [user_schema.dump(user) for user in User.query.all()]


class VistaSignUp(Resource):

    def post(self):
        # Crea un usuario en la aplicación: /users/signup
        try:
            try:
                user_username = User.query.filter(
                    User.username == request.json['username']).first()

                user_email = User.query.filter(
                    User.email == request.json['email']).first()

                user_pass = request.json['password']

            except Exception as e:
                return {'mensaje': 'Por favor ingresar todos los campos', 'error': str(e)}, 400

            if len(request.json['username'].strip()) == 0:
                return {'mensaje': 'El nombre de usuario no puede estar vacío'}, 400

            if len(request.json['email'].strip()) == 0:
                return {'mensaje': 'El correo electrónico no puede estar vacío'}, 400

            if len(request.json['password'].strip()) == 0:
                return {'mensaje': 'La contraseña puede estar vacía'}, 400

            if user_username is not None:
                return {'mensaje': 'Nombre de usuario ya existe, por favor iniciar sesión'}, 412

            if user_email is not None:
                return {'mensaje': 'Correo electronico ya existe, por favor iniciar sesión'}, 412

            salt = uuid.uuid4().hex
            password_hash = encrypt(salt, user_pass)

            new_user = User(username=request.json['username'],
                            email=request.json['email'],
                            password=password_hash,
                            salt=salt)

            db.session.add(new_user)
            db.session.commit()

            return {'id': new_user.id, 'createdAt': new_user.createdAt.isoformat(timespec='seconds')}, 201

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class VistaPong(Resource):

    def get(self):
        # Retorna pong: /
        return 'pong', 200
    
class VistaPongUsers(Resource):

    def get(self):
        # Retorna pong: /
        return 'pong desde users', 200
