# init_db.py

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from application.backend.database import SessionLocal, Base, engine
from application.backend.models import User, Product
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from pathlib import Path


base_dir = Path(__file__).resolve().parents[2]
env_path = base_dir / "labs" / "06_07_08_test_framework" / ".env"
load_dotenv(dotenv_path=env_path, override=True)


# Ladda miljövariabler från .env
admin_user = os.getenv("admin_username")
admin_pass = os.getenv("admin_password")

# Setup för lösenordshashning
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Skapa admin-användare från .env
def create_admin(db):
    if not admin_user or not admin_pass:
        print("admin_username eller admin_password saknas i .env!")
        return

    existing_user = db.query(User).filter(User.username == admin_user).first()
    if not existing_user:
        admin = User(username=admin_user, hashed_password=get_password_hash(admin_pass))
        db.add(admin)
        db.commit()
        print("Admin-användare skapad.")
    else:
        print("Admin-användare finns redan.")


# Skapa vanliga användare med produkter
def seed_sample_users_and_products(db):
    sample_users = [
        {
            "username": "user83",
            "password": "Pass83",
            "products": ["backend programering 1", "frontend programering 1"],
        },
        {
            "username": "bob",
            "password": "password2",
            "products": ["testning av mjukvara 3"],
        },
        {"username": "charlie", "password": "password3", "products": []},
    ]

    for user_data in sample_users:
        existing_user = db.query(User).filter_by(username=user_data["username"]).first()
        if existing_user:
            print(f"🔹 Användare '{user_data['username']}' finns redan.")
            continue

        user = User(
            username=user_data["username"],
            hashed_password=get_password_hash(user_data["password"]),
        )

        db.add(user)  # Lägg till i session först
        db.flush()  # Se till att user.id är tillgängligt

        for product_name in user_data["products"]:
            product = db.query(Product).filter_by(name=product_name).first()
            if not product:
                product = Product(name=product_name)
                db.add(product)
                db.flush()  # Se till att product.id finns

            user.products.append(product)  # Nu fungerar relationen

    try:
        db.commit()
        print("Användare och produkter tillagda.")
    except IntegrityError:
        db.rollback()
        print("Fel vid tillägg av användare/produkter.")


# Skapa produkter (kurser) utan koppling till någon användare
def seed_products_without_users(db):
    courses = [
        "Python för nybörjare",
        "Avancerad Java-programmering",
        "CI/CD pipelines med Jenkins",
        "Agil utveckling och Scrum",
        "Automatiserade tester med Selenium",
    ]

    for course_name in courses:
        existing_product = db.query(Product).filter_by(name=course_name).first()
        if existing_product:
            print(f"🔹 Kursen '{course_name}' finns redan.")
            continue

        product = Product(name=course_name)
        db.add(product)

    try:
        db.commit()
        print("Kurser utan användare tillagda.")
    except IntegrityError:
        db.rollback()
        print("Fel vid tillägg av kurser utan användare.")


# Initiera databasen (körs från main.py)
def init_db():
    Base.metadata.create_all(bind=engine)  # Skapar tabeller
    db = SessionLocal()
    try:
        create_admin(db)
        seed_sample_users_and_products(db)
        seed_products_without_users(db)  # Lägg till kurser utan användare här
    finally:
        db.close()


def reset_db():
    print("Droppar alla tabeller...")
    Base.metadata.drop_all(bind=engine)
    print("Skapar om alla tabeller...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        create_admin(db)
        seed_sample_users_and_products(db)
        seed_products_without_users(db)
        print("Databasen återställd via DROP/CREATE.")
    except Exception as e:
        db.rollback()
        print(f"Fel vid reset_db: {e}")
    finally:
        db.close()
