from flask import Blueprint, jsonify

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/clients', methods=['GET'])
def get_clients():
    # Тут будет логика для получения клиентов из базы данных
    return jsonify({"clients": []}), 200
