"""API code."""
import os
from datetime import datetime

from analisator import is_victory
from flask import Flask, json, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from swagger import get_config_swagger, get_swagger_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saves.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    saves = db.relationship(
        'Saves',
        backref='Game',
        lazy='dynamic',
        cascade = 'all, delete, delete-orphan',
    )
    
    def __repr__(self):
        return '<Game %r>' % self.id

class Saves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    data_save = db.Column(db.JSON)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def __repr__(self):
        return '<Saves %r>' % self.id

class myResource(Resource):
    json_dict = {}
    
    @app.route('/specification')
    def create_swagger_spec():
        return get_swagger_data()
    
    @app.route('/new-game', methods=['POST'])
    def run_new_game():
        """
        Deletes all saves from database.

        Returns:
            dict
        """
        if request.is_json:
            json_dict = request.get_json()
        if not request.is_json:
            return 'No JSON data!', 404
        try:
            a = Game.query.filter_by(name=json_dict['game_name']).all()
            for _ in a:
                db.session.delete(_)
                db.session.commit()
            db.session.add(
                Game(
                    name=json_dict['game_name'],
                )
            )
            db.session.commit()
            res = Game.query.filter_by(name=json_dict['game_name']).all()
            res[0].saves.append(
                Saves(
                    name='name',
                    data_save=json.dumps(json_dict)
                )
            )
            db.session.commit()
        except:
            return 'error save'
        return 'Game started successfully!', 200

    @app.route('/new-step', methods=['POST'])
    def run_new_step():
        result = ''
        if request.is_json:
            json_dict = request.get_json()
            if is_victory((json_dict), 'cross'):
                result = 'Victory cross!'
            if is_victory((json_dict), 'round'):
                result = 'Victory round!'
        if not request.is_json:
            return 'No JSON data', 404
        try:
            res = Game.query.filter_by(name=json_dict['game_name']).all()
            res[0].saves.append(
                Saves(
                    name='name',
                    data_save=json.dumps(json_dict)
                )
            )
            db.session.commit()
        except:
            return 'error save'
        if result == '':
            result = 'New step saved!' 
        return result, 200


    #@app.route('/list')
    #def f():
    #    a = {game.id: game.name for game in Game.query.all()}
    #    b = {save.id: save.game_id for save in Saves.query.all()}
    #    return {'a': a, 'b': b}


    @app.route('/list-saves', methods=['POST'])
    def get_list_saves():
        """
        Returns a dictionary with a list of saved game situations.

        Returns:
            json
        """
        if request.is_json:
            json_dict = request.get_json()
        if not request.is_json:
            return 'No JSON data', 404
        res = Game.query.filter_by(name=json_dict['game_name']).all()
        res2 = Saves.query.filter_by(game_id=res[0].id).all()
        return json.dumps(
            {save.id: save.name for save in res2}
        )

    @app.route('/load_game/<int:id>', methods=['POST'])
    def load_game(id=0):
        """
        Sets the current game situation by ID and deletes all subsequent saves.

        Args:
            id: int

        Returns:
            dict
        """
        if request.is_json:
            json_dict = request.get_json()
        if not request.is_json:
            return 'No JSON data', 404
        res = Game.query.filter_by(name=json_dict['game_name']).all()
        res2 = Saves.query.filter_by(game_id=res[0].id).all()
        res_dict = {}
        for save in res2:
            if int(save.id) == id:
                res_dict = save.data_save
        return json.dumps(res_dict)


if __name__ == '__main__':
    if not os.path.exists('/home/user/API-tic-tac/instance/saves.db'):
        with app.app_context():
            db.create_all()
    api = Api(app)
    api.add_resource(myResource, '/')
    app.register_blueprint(get_config_swagger())
    app.run(debug=True, host='0.0.0.0')
