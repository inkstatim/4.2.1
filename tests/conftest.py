import pytest
import requests
from faker import Faker
from tests.constant import BASE_URL, HEADERS

fake = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture()
def created_booking(auth_session, booking_data):
    response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert response.status_code == 200
    booking_id = response.json().get("bookingid")
    assert booking_id
    return booking_id, booking_data