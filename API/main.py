"""API code."""
import os

from flask import Flask, request, json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saves.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Save(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    data_save = db.Column(db.JSON)

    def __repr__(self):
        return '<Save %r>' % self.id

#if os.path.exists('/API-tic-tac/instance/saves.db'):
#with app.app_context():
#    db.create_all()
    
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
            new_record = Save(
                name='save1',
                data_save=json.dumps(json_dict),
            )
            list_saves = Save.query.all()
            for _ in list_saves:
                print(_.name)
            try:
                db.session.add(new_record)
                db.session.commit()
            except:
                return 'error'
            return 'valid data', 200
        return 'no valid data', 404
    
    
    def put(self, ):
        return 'put', 200
    
    def delete(self, ):
        return 'delete', 200
        


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(myResource, '/tic-tac', '/tic-tac/')
    app.run(debug=True)
    
