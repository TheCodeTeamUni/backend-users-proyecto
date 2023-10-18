import uuid
from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, decode_token
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


class VistaLogin(Resource):

    def post(self):
        # Loguea un usuario en la aplicacion: /users/login

        try:
            try:
                user_email = request.json['email']
                user_pass = request.json['password']

            except Exception as e:
                return {'mensaje': 'Por favor ingresar todos los campos', 'error': str(e)}, 404

            usuario = User.query.filter(User.email == user_email).first()

            if len(request.json['email'].strip()) == 0 or len(request.json['password'].strip()) == 0:
                return {'mensaje': 'No puede tener campos vacios'}, 400

            if usuario is None:
                return {'mensaje': 'El usuario no existe'}, 404

            salt = usuario.salt
            user_pass = usuario.password
            input_pass = encrypt(salt, request.json['password'])

            if user_pass != input_pass:
                return {'mensaje': 'La contraseña es incorrecta'}, 401

            token_de_acceso = create_access_token(identity=usuario.id)
            expireAt = datetime.now() + timedelta(minutes=15)

            usuario.token = token_de_acceso
            usuario.expireAt = expireAt
            db.session.commit()

            return {'id': usuario.id, 'token': token_de_acceso, 'type': usuario.type}, 200

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class VistaUser(Resource):

    def get(self):
        # Retorna un usuario por su id: /users/me

        try:
            try:
                token = request.headers.get('Authorization', None)[7:]
            except:
                return {'mensaje': 'Por favor ingresar un token'}, 400

            valid_data = decode_token(token, allow_expired=True)
            userId = valid_data['sub']
            usuario = User.query.get_or_404(userId)

            processData = datetime.now().isoformat()

            tokenDate = datetime.fromtimestamp(
                int(valid_data['exp'])).isoformat()

            tokenBD = usuario.token

            if processData > tokenDate:
                return {'mensaje': 'El token esta vencido'}, 401

            if tokenBD != token:
                return {'mensaje': 'El token no es valido'}, 401

            return user_schema.dump(usuario), 200

        except Exception as e:
            return {'mensaje': 'Por favor ingresar un token valido'}, 401


class VistaValidateEmail(Resource):

    def post(self):
        try:
            user_email = User.query.filter(
                User.email == request.json['email']).first()
            
            if user_email is not None:
                return {'mensaje': 'Usuario ya existe'}, 400
            
            else:
                return {'mensaje': 'Usuario no existe'}, 200

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class VistaPong(Resource):

    def get(self):
        # Retorna pong si el servicio se encuentra en linea: /
        return 'pong users', 200
