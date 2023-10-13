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

    def test_get_users(self):

        newUser = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        headers = {'Content-Type': 'application/json'}

        users_before = self.client.get("/users/all", headers=headers)
        len_users_before = len(json.loads(users_before.get_data()))

        sol_newUser = self.client.post("/users/signup",
                                       data=json.dumps(newUser),
                                       headers={'Content-Type': 'application/json'})

        users_after = self.client.get("/users/all", headers=headers)
        len_users_after = len(json.loads(users_after.get_data()))

        self.assertEqual(len_users_before, 1)
        self.assertEqual(sol_newUser.status_code, 201)
        self.assertEqual(len_users_after, 2)

    def test_signup_user(self):

        newUser = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 201)

    def test_signup_error(self):

        newUser = {
            "username": 1234567,
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 503)

    def test_signup_missing(self):

        newUser = {
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 404)

    def test_signup_missing_data(self):

        newUser = {
            "username": '',
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        newUserTwo = {
            "username": self.data_factory.name(),
            "email": '',
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        newUserThree = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": '',
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        newUserFour = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": '',
            "type": ''
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(newUserTwo),
                                           headers=headers)

        sol_newUser_Three = self.client.post(endpoint_usuario,
                                             data=json.dumps(newUserThree),
                                             headers=headers)

        sol_newUser_Four = self.client.post(endpoint_usuario,
                                            data=json.dumps(newUserFour),
                                            headers=headers)

        self.assertEqual(sol_newUser.status_code, 400)
        self.assertEqual(sol_newUser_Two.status_code, 400)
        self.assertEqual(sol_newUser_Three.status_code, 400)
        self.assertEqual(sol_newUser_Four.status_code, 400)

    def test_signup_fail_password(self):
        newUser = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": "password",
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 400)

    def test_signup_existent_user(self):

        newUserTwo = {
            "username": self.user_username,
            "email": self.data_factory.email(),
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        newUserThree = {
            "username": self.data_factory.name(),
            "email": self.user_email,
            "password": self.data_factory.password(),
            "type": self.data_factory.random_element(elements=('1', '2'))
        }

        endpoint_usuario = "/users/signup"
        headers = {'Content-Type': 'application/json'}

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(newUserTwo),
                                           headers=headers)

        sol_newUser_Three = self.client.post(endpoint_usuario,
                                             data=json.dumps(newUserThree),
                                             headers=headers)

        self.assertEqual(sol_newUser_Two.status_code, 400)
        self.assertEqual(sol_newUser_Three.status_code, 400)

    def test_ping_users(self):

        endpoint_ping = "/"
        headers = {'Content-Type': 'application/json'}

        sol_ping = self.client.get(endpoint_ping,
                                   headers=headers)

        self.assertEqual(sol_ping.status_code, 200)
