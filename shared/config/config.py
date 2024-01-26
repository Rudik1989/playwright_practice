from os import path

import yaml


def _load_default_config():
    default_config_name = 'default.yaml'
    config_path = path.join(path.dirname(__file__), default_config_name)
    with open(config_path, 'r') as default_config:
        config = yaml.full_load(default_config)
    return config


shared_config = _load_default_config()
