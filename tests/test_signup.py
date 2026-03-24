from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    activities[activity_name]["participants"] = [
        participant
        for participant in activities[activity_name]["participants"]
        if participant != email
    ]

    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_removes_existing_participant():
    activity_name = "Chess Club"
    email = "remove-me@mergington.edu"

    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]