from flask import Flask, send_file, request
""" from config import config """
from red import Red

#Routes
from routes import Topologia, Correos, Usuarios, rip, ospf, eigrp, BajaProtocolo

app = Flask(__name__)

@app.get('/')
def index():
    return send_file('static/index.html')

@app.post('/topologia')
def obtenerTopoliga():
    """ Obetener la topologia de la red e inicializa los 
    datos del router al que primero se conecta """
    # Obteniendo credenciales desde la petición
    credenciales = request.get_json()
    ip = credenciales['ip']
    name = credenciales['name']
    user = credenciales['user']
    password = credenciales['password']
    
    # Asignando crecentiales a la red
    global red 
    red = Red(ip, name, user, password)
    
    # Leyendo la topologia
    red.leerTopologia() # almacena en el archivo topologia.jpg
    
    return send_file('static/topologia.jpg')


def page_not_found(error):
    return "<h1>Pagina no encontrada</h1>"

if __name__ == '__main__':
    """ app.config.from_object(config['development']) """

    # Blueprints
    app.register_blueprint(Usuarios.main,url_prefix = '/api/usuarios')
    #app.register_blueprint(Topologia.main,url_prefix = '/api/topologia')
    app.register_blueprint(rip.main, url_prefix = '/api/rip')
    app.register_blueprint(ospf.main, url_prefix = '/api/ospf')
    app.register_blueprint(eigrp.main, url_prefix = '/api/eigrp')
    app.register_blueprint(BajaProtocolo.main, url_prefix = '/api/baja-protocolo')
    app.register_blueprint(Correos.main, url_prefix = '/api/correo')

    app.register_error_handler(404, page_not_found)
    app.run(debug = True)
