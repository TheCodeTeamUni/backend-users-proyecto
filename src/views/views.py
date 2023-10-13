import uuid
from flask_restful import Resource
from flask import request
from ..models import db, User, UserSchema
from ..utils import encrypt, validate_password

user_schema = UserSchema()


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

                user_type = request.json['type']

            except Exception as e:
                return {'mensaje': 'Por favor ingresar todos los campos', 'error': str(e)}, 404

            if (len(request.json['email'].strip()) == 0 or
                len(request.json['username'].strip()) == 0 or
                len(request.json['password'].strip()) == 0 or
                    len(request.json['type'].strip()) == 0):

                return {'mensaje': 'No puede tener campos vacios'}, 400

            if user_username is not None or user_email is not None:
                return {'mensaje': 'Usuario ya existe'}, 400

            if not validate_password(user_pass):
                return {'mensaje': 'La contraseña no cumple los requisitos'}, 400

            salt = uuid.uuid4().hex
            password_hash = encrypt(salt, user_pass)

            new_user = User(username=request.json['username'],
                            email=request.json['email'],
                            password=password_hash,
                            salt=salt,
                            type=user_type)

            db.session.add(new_user)
            db.session.commit()

            return {'id': new_user.id, 'createdAt': new_user.createdAt.isoformat(timespec='seconds')}, 201

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class ViewUsers(Resource):

    def get(self):
        # Retorna todos los usuarios registrados: /users/all
        return [user_schema.dump(user) for user in User.query.all()]


class VistaPong(Resource):

    def get(self):
        # Retorna pong: /
        return 'pong', 200


class VistaPongUsers(Resource):

    def get(self):
        # Retorna pong: /
        return 'pong desde users', 200
