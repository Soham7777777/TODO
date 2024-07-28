import pytest
from instance import Testing
from Application import create_app
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Flask:
    app = create_app(Testing())
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()