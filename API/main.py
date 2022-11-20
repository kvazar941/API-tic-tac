"""API code."""
from flask import Flask, request, json
from flask_restful import Api, Resource, reqparse

GAME_DATA = {
    'number of cage to win': None,
    'cages': [
        {
            'x': 0,
            'y': 0,
            'condition': None,
        },
        {
            'x': 0,
            'y': 1,
            'condition': None,
        },
        {
            'x': 1,
            'y': 0,
            'condition': None,
        },
    ],
}


class Cage():
    def __init__(x, y, condition):
        self.x = 0
        self.y = 0
        self.condition = None


class myResource(Resource):
    def get(self, ):
        if request.is_json:
            json_dict = request.get_json()
            print(request.method)
            return 'valid data', 200
        return 'no valid data', 404
    
    
    def put(self, ):
        return 'put', 200
    
    def delete(self, ):
        return
        


if __name__ == '__main__':
    # Создаем приложение
    app = Flask(__name__)
    # Создаем интерфейс, используем Api и ссылаемся на наше приложение
    api = Api(app)
    # Добавляем к Api ресурс (класс 'myResource', в котором будут существовать свои методы), список URL, по которым доступны ответы сервера.
    api.add_resource(myResource, '/tic-tac', '/tic-tac/')
    # Запускаем приложение
    app.run(debug=True)
    
