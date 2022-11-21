"""API code."""
import os

from flask import Flask, request, json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from fixtures import GAME_START_SITUATION


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

if not os.path.exists('/home/user/API-tic-tac/instance/saves.db'):
    with app.app_context():
        db.create_all()


class myResource(Resource):
    json_dict = {}
    
    @app.route('/new-game')
    def new_game():
        for save in Save.query.all():
            db.session.delete(save)
        db.session.commit()
        return '', 200


    def save_game(self, name, data):
        try:
            db.session.add(Save(name=name, data_save=json.dumps(data)))
            db.session.commit()
        except:
            return 'error save'

    @app.route('/load_game/<int:id>')
    def load_game(self, id=0):
        for save in Save.query.all():
            if save.id > id:
                db.session.delete(save)
            if save.id == id:
                json_dict = save.data_save
        db.session.commit()
        return json_dict
    
    
    def is_victory(self, _dict):
        print(_dict)
        return True
    
    
    @app.route('/list-saves')
    def get_list_saves():
        return {save.id: save.name for save in Save.query.all()}


    def get(self, ):
        if request.is_json:
            self.json_dict = request.get_json()
            if self.is_victory(self.json_dict):
                return 'Victory cross!', 200
            self.save_game('Step', self.json_dict)
            return '', 200
        return '', 404


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(myResource, '/tic-tac', '/tic-tac/')
    app.run(debug=True)
    
