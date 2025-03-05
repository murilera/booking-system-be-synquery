import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def sample_booking():
    return {
        "name": "John Doe",
        "profession": "Electrician",
        "date": "2025-06-15",
        "time": "14:00",
    }


def test_create_booking(sample_booking):
    response = client.post(
        "/process_command",
        json={
            "command": f"Book {sample_booking['profession']} {sample_booking['name']} on {sample_booking['date']} at {sample_booking['time']}"
        },
    )
    assert response.status_code == 200
    assert "booking" in response.json()


def test_duplicate_booking(sample_booking):
    client.post(
        "/process_command",
        json={
            "command": f"Book {sample_booking['profession']} {sample_booking['name']} on {sample_booking['date']} at {sample_booking['time']}"
        },
    )
    response = client.post(
        "/process_command",
        json={
            "command": f"Book {sample_booking['profession']} another person on {sample_booking['date']} at {sample_booking['time']}"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Time slot already booked for this technician."


def test_list_bookings():
    response = client.get("/bookings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_booking():
    response = client.get("/bookings")
    if response.json():
        booking_id = response.json()[0]["id"]
        delete_response = client.delete(f"/booking/{booking_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "Booking deleted successfully"}
