from fastapi.testclient import TestClient
from db import engine
from main import app
import pytest
from orm.user import User, Role
from sqlmodel import SQLModel, Session, select

client = TestClient(app)

TEST_USER_DATA = {
    "first_name": "Test",
    "last_name": "User",
    "email": "user@example.com",
    "password": "123456",
    "phone": "1234567890"
}

TEST_AUTHOR_DATA = {
    "first_name": "Test",
    "last_name": "Author",
    "biography": "Test biography",
    "birth_date": "2001-01-01T00:00:00"
}

TEST_BOOK_DATA = {
    "title": "Test Book",
    "publication_year": 2025,
    "page_count": 100,
    "description": "Test description",
    "image_url": "http://example.com/test.jpg",
    "publisher_id": 1
}

TEST_GENRE_DATA = {
    "name": "Test Genre",
    "description": "Test genre description"
}

TEST_PUBLISHER_DATA = {
    "name": "Test Publisher",
    "address": "Test Address",
    "phone": "1234567890"
}

@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db_session:
        yield db_session

@pytest.fixture
def user_token(session: Session):
    register_response = client.post("/register", data=TEST_USER_DATA)
    assert register_response.status_code == 200

    user = session.exec(
        select(User).where(User.email == TEST_USER_DATA["email"])
    ).first()
    assert user is not None

    user.role = Role.MODERATOR
    session.add(user)
    session.commit()

    login_response = client.post("/login", data={
        "username": TEST_USER_DATA["email"],
        "password": TEST_USER_DATA["password"]
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data

    yield token_data["access_token"]

    session.delete(user)
    session.commit()

def test_book(user_token):
    # Создаем автора
    response = client.post("/authors", json=TEST_AUTHOR_DATA, headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    author = response.json()
    assert author["first_name"] == TEST_AUTHOR_DATA["first_name"]
    assert author["last_name"] == TEST_AUTHOR_DATA["last_name"]

    # Обновляем автора
    author_id = author["id"]
    update_data = { "first_name": "Updated First Name" }
    response = client.put(f"/authors/{author_id}", json=update_data, headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    updated_author = response.json()
    assert updated_author["first_name"] == update_data["first_name"]

    # Создаем жанр
    response = client.post("/genres", json=TEST_GENRE_DATA, headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    genre = response.json()
    assert genre["name"] == TEST_GENRE_DATA["name"]

    # Создаем издателя
    response = client.post("/publishers", json=TEST_PUBLISHER_DATA, headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    publisher = response.json()
    assert publisher["name"] == TEST_PUBLISHER_DATA["name"]

    # Создаем книгу
    book_data = {**TEST_BOOK_DATA, "publisher_id": publisher["id"]}
    response = client.post("/books", json=book_data, headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == book_data["title"]

    # Добавляем автора к книге
    response = client.post(f"/books/{book['id']}/authors/{author['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200

    # Добавляем жанр к книге
    response = client.post(f"/books/{book['id']}/genres/{genre['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200

    client.delete(f"/publishers/{publisher['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })

    client.delete(f"/genres/{genre['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })

    client.delete(f"/authors/{author['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })

    client.delete(f"/books/{book['id']}", headers={
        "Authorization": f"Bearer {user_token}"
    })
