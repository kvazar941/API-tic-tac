"""API code."""
import os
from datetime import datetime

from analisator import is_victory
from flask import Flask, json, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

import yaml

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saves.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SWAGGER_URL = '/api/docs'
API_URL = '/swagger'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My App'
    }
)


class Save(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    data_save = db.Column(db.JSON)

    def __repr__(self):
        return '<Save %r>' % self.id


class myResource(Resource):
    json_dict = {}
    
    @app.route('/swagger')
    def create_swagger_spec():
        with open('./API/api/docs/swagger.yaml') as file_name:
            file_content = file_name.read()
        return yaml.safe_load(file_content)

    def save_game(self, name, situation):
        try:
            db.session.add(Save(name=name, data_save=json.dumps(situation)))
            db.session.commit()
        except:
            return 'error save'

    @app.route('/list-saves')
    def get_list_saves():
        """
        Returns a dictionary with a list of saved game situations.

        Returns:
            json
        """
        return json.dumps({save.id: save.name for save in Save.query.all()})

    @app.route('/new-game')
    def new_game():
        """
        Deletes all saves from database.

        Returns:
            dict
        """
        for save in Save.query.all():
            db.session.delete(save)
        db.session.commit()
        return '', 200

    @app.route('/load_game/<int:id>')
    def load_game(self, id=0):
        """
        Sets the current game situation by ID and deletes all subsequent saves.

        Args:
            id: int

        Returns:
            dict
        """
        for save in Save.query.all():
            if save.id > id:
                db.session.delete(save)
            if save.id == id:
                json_dict = save.data_save
        db.session.commit()
        return json_dict

    def get(self):
        """
        Check if the situation is winning for one of the players and if not, save the result in the database.

        Returns:
            str, int
        """
        if request.is_json:
            self.json_dict = request.get_json()
            if is_victory((self.json_dict), 'cross'):
                return 'Victory cross!', 200
            if is_victory((self.json_dict), 'round'):
                return 'Victory round!', 200
            self.save_game('Step', self.json_dict)
            return '', 200
        return '', 404


if __name__ == '__main__':
    if not os.path.exists('/home/user/API-tic-tac/instance/saves.db'):
        with app.app_context():
            db.create_all()
    api = Api(app)
    api.add_resource(myResource, '/')
    app.register_blueprint(swaggerui_blueprint)
    app.run(debug=True, host='0.0.0.0')
