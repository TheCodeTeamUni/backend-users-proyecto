from src import create_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from src.models import db
from src.views import ViewUsers, VistaSignUp, VistaPong, VistaLogin

application = create_app('default')
app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)
api.add_resource(ViewUsers, '/users/all')
api.add_resource(VistaSignUp, '/users/signup')
api.add_resource(VistaLogin, '/users/login')
api.add_resource(VistaPong, '/')

jwt = JWTManager(application)

@application.errorhandler(404)
def page_not_found(e):
    # your processing here
    return 'Pagina no encontrada', 404

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 3001, debug = True)