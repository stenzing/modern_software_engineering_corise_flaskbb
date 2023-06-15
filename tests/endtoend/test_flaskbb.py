import flask
import pytest
from flaskbb import create_app
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.extensions import db
from flaskbb.utils.populate import create_default_groups, create_default_settings
from flaskbb.utils.translations import compile_translations
from playwright.sync_api import Page, expect

###################################################################
# CoRise TODO: add a new fixture `translations` that calls the
# `compile_translations` function from flaskbb.utils.translations

# ADD CODE HERE

@pytest.fixture(scope="session")
def app():
    # Hint: create the app, and setup any default context like translations,
    # settings, DB, etc.
    # Hint: take a look at the tests/fixtures/app.py file for the details of 
    # how to configure the application.
    # TODO: ADD CODE HERE
    app = create_app(Config)

    with app.app_context():
        db.create_all()
        create_default_groups()
        create_default_settings()
        compile_translations()

    return app


def test_load_home_page(live_server, page: Page):
    # Hint: Check out `flask.url_for` helper function to get the external url for 
    # an endpoint. Then go to it using playwright's `page.goto(url)`
    # TODO: ADD CODE HERE
    page.goto(url=flask.url_for(".index", _external=True))

    expect(page).to_have_title(" FlaskBB - A lightweight forum software in Flask ")

###################################################################