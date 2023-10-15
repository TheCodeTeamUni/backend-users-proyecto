import json
from unittest import TestCase
from faker import Faker
from application import application as app
from src.models import User, db


class TestUsuario(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.user_pass = self.data_factory.password()
        self.user_username = self.data_factory.name()
        self.user_email = self.data_factory.email()
        self.type = self.data_factory.random_element(elements=('1', '2'))

        newUser = {
            "username": self.user_username,
            "email": self.user_email,
            "password": self.user_pass,
            "type": self.type
        }

        sol_newUser = self.client.post("/users/signup",
                                       data=json.dumps(newUser),
                                       headers={'Content-Type': 'application/json'})

        respuestaUser = json.loads(sol_newUser.get_data())

        self.user_id = respuestaUser["id"]
        self.user_createdAt = respuestaUser["createdAt"]

    def tearDown(self):

        usuarios = User.query.all()
        for usuario in usuarios:
            db.session.delete(usuario)

        db.session.commit()

    def test_login_user(self):

        loginUser = {
            "email": self.user_email,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_logUser.status_code, 200)

    def test_login_error(self):

        loginUser = {
            "email": 123456789,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_logUser.status_code, 503)

    def test_login_missing(self):

        loginUser = {
            "email": self.user_email,
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_logUser.status_code, 404)

    def test_login_missing_data(self):

        loginUser = {
            "email": '',
            "password": self.user_pass
        }

        loginUserTwo = {
            "email": '',
            "password": self.user_pass
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        sol_logUserTwo = self.client.post(endpoint_usuario,
                                          data=json.dumps(loginUserTwo),
                                          headers=headers)

        self.assertEqual(sol_logUser.status_code, 400)
        self.assertEqual(sol_logUserTwo.status_code, 400)

    def test_login_user_wrong_email(self):

        loginUser = {
            "email": self.user_email + "wrong",
            "password": self.user_pass
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_logUser.status_code, 404)

    def test_login_user_wrong_password(self):

        loginUser = {
            "email": self.user_email,
            "password": self.user_pass + "wrong"
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_logUser.status_code, 401)

    def test_fail_page(self):

        endpoint_usuario = "/users/fail"
        headers = {'Content-Type': 'application/json'}

        sol_logUser = self.client.get(endpoint_usuario,
                                      headers=headers)

        self.assertEqual(sol_logUser.status_code, 404)