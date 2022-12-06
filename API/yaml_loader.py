"""yaml_loader module."""
import yaml


def read_file(url):
    with open(url) as file_name:
        file_content = file_name.read()
    return yaml.safe_load(file_content)
