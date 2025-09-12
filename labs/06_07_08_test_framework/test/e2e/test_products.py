from dotenv import load_dotenv
import sys
import os

# Lägg till projektroten (där 'application' mappen finns) i sys.path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from playwright.sync_api import Page
from models.ui.home import HomePage
from models.ui.admin import AdminPage
from models.ui.user import UserPage
from models.api.user import UserAPI
from models.api.admin import AdminAPI
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


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)


# Then The product is available to be used in the app
def test_add_product_to_catalog(page: Page):
    user_api = UserAPI(os.getenv("BASE_URL"))
    username = os.getenv("admin_username")
    password = os.getenv("admin_password")
    home_page = HomePage(page)
    admin_page = AdminPage(page)
    user_page = UserPage(page)
    token = user_api.login_token(username, password)
    page.add_init_script(f"window.localStorage.setItem('token', '{token}')")
    # Given I am an admin user​
    home_page.navigate()
    # When I add a product to the catalog​
    admin_page.create_product("Java-programmering för nybörjare")
    # complete code
    user_page.logout()


def test_remove_product_from_catalog(page: Page):
    user_api = UserAPI(os.getenv("BASE_URL"))
    admin_api = AdminAPI(os.getenv("BASE_URL"))
    # Given I am an admin user​
    username = os.getenv("admin_username")
    password = os.getenv("admin_password")
    home_page = HomePage(page)
    admin_page = AdminPage(page)
    user_page = UserPage(page)
    token = user_api.login_token(username, password)
    page.add_init_script(f"window.localStorage.setItem('token', '{token}')")
    admin_api.set_token(token)
    if (
        admin_api.get_product_by_name("Java-programmering för nybörjare")
        == "Java-programmering för nybörjare"
    ):
        admin_api.delete_product_by_name(
            "Java-programmering för nybörjare"
        )  # tar bort restproduct från add product testet.
    else:
        pass
    home_page.navigate()
    # When I remove a product from the catalog​
    admin_page.delete_product_by_name("CI/CD pipelines med Jenkins")
    # Then The product should not be listed in the app to be used
    # complete code
    user_page.logout()
