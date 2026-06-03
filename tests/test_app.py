from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activity_list():
    # Arrange
    activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert activity in data
    assert isinstance(data[activity]["participants"], list)


def test_signup_adds_participant_to_activity():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in client.get("/activities").json()[activity]["participants"]


def test_unregister_removes_participant_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_nonexistent_participant_returns_400():
    # Arrange
    activity = "Chess Club"
    email = "missingstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unknown_activity_returns_404_for_signup():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unknown_activity_returns_404_for_unregister():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
