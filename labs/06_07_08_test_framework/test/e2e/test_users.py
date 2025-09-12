import sys
import os

# Lägg till projektroten (där 'application' mappen finns) i sys.path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Lägg till projektets rotmapp (där application/ ligger) till sys.path
from playwright.sync_api import Page
from models.ui.home import HomePage
from models.ui.user import UserPage
from models.ui.signup import SignupPage
from models.api.user import UserAPI
from application.backend.init_db import reset_db
from application.backend.database import SessionLocal
from application.backend.models import User
import pytest
import libs.utils
# complete imports


# Fixture som resetar databasen före varje test
@pytest.fixture(autouse=True)
def setup_database():
    reset_db()
    yield


def test_signup(page: Page):
    user_page = UserPage(page)
    home_page = HomePage(page)
    signup_page = SignupPage(page)
    # Given I am a new potential customer​
    username = libs.utils.generate_string_with_prefix()
    password = "GenUserpass25"
    home_page.navigate()
    home_page.go_to_signup()
    signup_page.signup(username, password)
    # When I signup in the app​
    signup_page.go_to_home()
    home_page.login(username, password)
    # Then I should be able to log in with my new user
    # assert?
    user_page.logout()


def test_signin(page: Page):
    user_page = UserPage(page)
    home_page = HomePage(page)
    # Given I am an authenticated user​
    username = "user83"
    password = "Pass83"
    home_page.navigate()
    # When I log in into the application​
    home_page.login(username, password)
    # Then I should see all my products
    # assert?
    user_page.logout()
