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

    def test_user_successful(self):

        loginUser = {
            "email": self.user_email,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/login"
        headers = {'Content-Type': 'application/json'}

        sol_login = self.client.post(endpoint_usuario,
                                     data=json.dumps(loginUser),
                                     headers=headers)

        respuestaUser = json.loads(sol_login.get_data())
        token = respuestaUser["token"]

        endpoint_me = "/users/me"
        headers_token = {'Content-Type': 'application/json',
                         "Authorization": "Bearer {}".format(token)}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_token)

        respuestaMe = json.loads(sol_me.get_data())

        self.assertEqual(sol_login.status_code, 200)
        self.assertEqual(sol_me.status_code, 200)
        self.assertEqual(respuestaMe["email"], self.user_email)

    def test_user_fallido(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmF' + \
                'sc2UsImlhdCI6MTY3NTgyMTY4NSwianRpIjoiOGEyY2JiNTAtND' + \
                'AyYi00OTM5LWIwYmUtODU2M2RhMWEyODdjIiwidHlwZSI6ImFjY2' + \
                'VzcyIsInN1YiI6MSwibmJmIjoxNjc1ODIxNjg1LCJleHAiOjE2Nz' + \
                'U4MjI1ODV9.KbV7iOfk6xhd_9C-j7nVyjrLoP-_MyJdKP87b708_kE'

        endpoint_me = "/users/me"
        headers_me = {'Content-Type': 'application/json',
                      "Authorization": "Bearer {}".format(token)}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_me)

        self.assertEqual(sol_me.status_code, 401)

    def test_user_fail(self):
        token = ''

        endpoint_me = "/users/me"
        headers_token = {'Content-Type': 'application/json',
                         "Authorization": "Bearer {}".format(token)}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_token)

        self.assertEqual(sol_me.status_code, 401)

    def test_missing_token(self):

        endpoint_me = "/users/me"
        headers_token = {'Content-Type': 'application/json'}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_token)

        self.assertEqual(sol_me.status_code, 400)

    def test_valida_email_success(self):

        endpoint_validate = "/users/validate"
        headers = {'Content-Type': 'application/json'}

        sol_validate = self.client.get(endpoint_validate,
                                       data=json.dumps(
                                           {"email": self.user_email}),
                                       headers=headers)

        respuestaValidate = json.loads(sol_validate.get_data())

        self.assertEqual(sol_validate.status_code, 400)
        self.assertEqual(respuestaValidate["mensaje"], "Usuario ya existe")

    def test_valida_email_fail(self):

        endpoint_validate = "/users/validate"
        headers = {'Content-Type': 'application/json'}

        sol_validate = self.client.get(endpoint_validate,
                                       data=json.dumps({"email": "email.com"}), headers=headers)

        respuestaValidate = json.loads(sol_validate.get_data())

        self.assertEqual(sol_validate.status_code, 200)
        self.assertEqual(respuestaValidate["mensaje"], "Usuario no existe")

    def test_valida_email_error(self):
        endpoint_validate = "/users/validate"
        headers = {'Content-Type': 'application/json'}

        sol_validate = self.client.get(endpoint_validate, headers=headers)

        self.assertEqual(sol_validate.status_code, 503)
