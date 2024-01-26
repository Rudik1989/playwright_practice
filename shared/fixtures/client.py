from pytest import fixture

from shared.client import SharedClient


@fixture(scope='session')
def client():
    return SharedClient
