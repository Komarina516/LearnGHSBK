from urllib.parse import quote


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity(client):
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"

    refreshed = client.get("/activities").json()
    assert new_email in refreshed[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant(client):
    activity_name = "Basketball Team"
    participant_email = "alex@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": participant_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {participant_email} from {activity_name}"

    refreshed = client.get("/activities").json()
    assert participant_email not in refreshed[activity_name]["participants"]


def test_unregister_missing_participant_returns_400(client):
    activity_name = "Basketball Team"
    missing_email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": missing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in this activity"
