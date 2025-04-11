from tests.constant import BASE_URL
import requests

class TestBookings:

    def test_get_all_bookings(self):
        response = requests.get(f"{BASE_URL}/booking")
        assert response.status_code == 200
        assert isinstance(response.json(), list), "Ответ должен быть списком"

    def test_put_update_booking(self, auth_session, created_booking):
        booking_id, _ = created_booking
        updated_data = {
            "firstname": "Updated",
            "lastname": "User",
            "totalprice": 777,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2024-04-10",
                "checkout": "2024-04-12"
            },
            "additionalneeds": "Late checkout"
        }

        response = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["firstname"] == "Updated"
        assert data["lastname"] == "User"
        assert data["totalprice"] == 777

    def test_patch_update_booking(self, auth_session, created_booking):
        booking_id, _ = created_booking
        patch_data = {"firstname": "Patched", "totalprice": 555}
        response = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=patch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["firstname"] == "Patched"
        assert data["totalprice"] == 555

    def test_put_non_existing_booking(self, auth_session):
        updated_data = {
            "firstname": "Ghost",
            "lastname": "NotReal",
            "totalprice": 1,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
            "additionalneeds": "None"
        }
        response = auth_session.put(f"{BASE_URL}/booking/999999", json=updated_data)
        assert response.status_code in [404, 405]

    def test_patch_without_auth(self, booking_data):
        response = requests.patch(f"{BASE_URL}/booking/1", json={"firstname": "Hacker"})
        assert response.status_code == 403, "Ожидался статус 403 при попытке патча без авторизации"

    def test_put_without_auth(self, booking_data):
        response = requests.put(f"{BASE_URL}/booking/1", json=booking_data)
        assert response.status_code == 403, "Ожидался статус 403 при попытке put без авторизации"