from flask import Flask
from config import config

#Routes
from routes import Topologia, Correos

app = Flask(__name__)

def page_not_found(error):
    return "<h1>Pagina no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(Topologia.main,url_prefix = '/api/topologia')
    app.register_blueprint(Correos.main, url_prefix = '/api/correo')

    app.register_error_handler(404, page_not_found)
    app.run()
