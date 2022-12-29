from flask import Blueprint, jsonify

main = Blueprint('Correos_blueprint',__name__)

@main.route('/')
def get_correos():
    return jsonify({'message': 'Aqui los correos el punto 10'})