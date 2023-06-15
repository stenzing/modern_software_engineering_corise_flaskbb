###################################################################
# CoRise TODO: add an integration test that uses the test client to
# load the home page ('/'). Make sure the response code is 200 and
# that the response data contains something you expect to see on the
# home page.
#
# Hint: you can get the test client by calling `application.test_client()`
# when using the application test fixture.

# ADD CODE HERE

from flask import Flask
import pytest

@pytest.mark.usefixtures("default_groups", "default_settings", "guest", "translations")
def test_page_load( application:Flask):
    resp = application.test_client().get('/')

    assert resp.status_code == 200
    assert "FlaskBB - A lightweight forum software in Flask" in resp.get_data(True)

###################################################################