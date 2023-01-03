from flask import Blueprint, jsonify

main = Blueprint('protocolos_blueprint',__name__)

@main.route('/')
def get_protocolos():
    return jsonify({'message': 'Aqui los protocolos'})