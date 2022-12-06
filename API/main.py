"""API code."""
import os

from analisator import is_victory
from flask import Flask, json, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from swagger import get_config_swagger, get_swagger_data

DATABASE_URL = '/home/user/API-tic-tac/instance/saves.db'

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


class Saves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    data_save = db.Column(db.JSON)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))


def add_record(record):
    db.session.add(record)
    db.session.commit()


def delete_record(record):
    db.session.delete(record)
    db.session.commit()


def add_game(game_name):
    for record in Game.query.filter_by(name=game_name).all():
        delete_record(record)
    add_record(Game(name=game_name))


def add_save_to_game(json_dict, game_name):
    game = Game.query.filter_by(name=game_name).first()
    saves = Saves.query.filter_by(game_id=game.id).all()
    call_saves = len([save.id for save in saves]) + 1
    save = Saves(
        name='Step {0}'.format(call_saves),
        data_save=json.dumps(json_dict),
    )
    game.saves.append(save)
    db.session.commit()


def create_database():
    if not os.path.exists(DATABASE_URL):
        with app.app_context():
            db.create_all()


class myResource(Resource):

    @app.route('/specification')
    def create_swagger_spec():
        return get_swagger_data()

    @app.route('/new-game', methods=['POST'])
    def make_new_game():
        """
        Make new game.

        Returns:
            str
        """
        if not request.is_json:
            return 'No JSON data!', 404
        json_dict = request.get_json()
        game_name = json_dict['game_name']
        try:
            add_game(game_name)
            add_save_to_game(json_dict, game_name)
        except:
            return 'Error save to database', 404
        return 'Game started successfully!', 200

    @app.route('/new-step', methods=['POST'])
    def run_new_step():
        if not request.is_json:
            return 'No JSON data', 404
        result_response = ''
        json_dict = request.get_json()
        game_name = json_dict['game_name']
        if is_victory((json_dict), 'cross'):
            result_response = 'Victory cross!'
        if is_victory((json_dict), 'round'):
            result_response = 'Victory round!'
        try:
            add_save_to_game(json_dict, game_name)
        except:
            return 'Error save to database', 404
        if result_response == '':
            result_response = 'New step saved!'
        return result_response, 200

    @app.route('/list-saves', methods=['POST'])
    def get_list_saves():
        """
        Returns a dictionary with a list of saved game situations.

        Returns:
            json
        """
        if not request.is_json:
            return 'No JSON data', 404
        json_dict = request.get_json()
        game_name = json_dict['game_name']
        game = Game.query.filter_by(name=game_name).first()
        saves = Saves.query.filter_by(game_id=game.id).all()
        return json.dumps(
            {save.id: save.name for save in saves},
        )

    @app.route('/load_game/<int:id>', methods=['POST'])
    def load_game(id=0):
        """
        Sets the current game situation by ID.

        Returns:
            dict
        """
        if not request.is_json:
            return 'No JSON data', 404
        json_dict = request.get_json()
        game_name = json_dict['game_name']
        game = Game.query.filter_by(name=game_name).first()
        saves = Saves.query.filter_by(game_id=game.id).all()
        for save in saves:
            if int(save.id) == id:
                return json.dumps(save.data_save)
        return 'No such data', 404


if __name__ == '__main__':
    create_database()
    api = Api(app)
    api.add_resource(myResource, '/')
    app.register_blueprint(get_config_swagger())
    app.run(debug=True, host='0.0.0.0')
