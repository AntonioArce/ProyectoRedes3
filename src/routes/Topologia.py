from flask import Blueprint, jsonify

main = Blueprint('topologia_blueprint',__name__)

@main.route('/')
def get_topoliga():
    return jsonify({'message': 'Aqui la topologia'})
