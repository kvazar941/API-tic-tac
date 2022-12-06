"""swagger code."""
from flask_swagger_ui import get_swaggerui_blueprint
from yaml_loader import read_file

SWAGGER_URL = '/api/docs'
API_URL = '/specification'
YAML_TO_SWAGGER_URL = './API/api/docs/swagger.yaml'


def get_config_swagger():
    return get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Api tic-tac'
        }
    )

def get_swagger_data():
    return read_file(YAML_TO_SWAGGER_URL)
