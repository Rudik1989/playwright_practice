import pytest

from shared.config.config import shared_config


@pytest.fixture(scope='function')
def open_browser(client):
    client.open_browser()
    client.go_to(shared_config['base-url'])
    yield client
    client.close()
