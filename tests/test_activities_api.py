from urllib.parse import quote

import pytest

import src.app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = app_module.activities

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{activity_path}/signup?email=newstudent@mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


@pytest.mark.parametrize(
    "endpoint_template",
    [
        "/activities/{activity_name}/unregister?email={email}",
        "/activities/{activity_name}/participants?email={email}",
        "/activities/{activity_name}/participants/{email}",
    ],
)
def test_unregister_removes_student_from_activity(client, endpoint_template):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    app_module.activities[activity_name]["participants"].append(email)
    endpoint = endpoint_template.format(
        activity_name=quote(activity_name, safe=""),
        email=quote(email, safe=""),
    )

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_path = quote("Unknown Club", safe="")

    # Act
    response = client.delete(
        f"/activities/{activity_path}/unregister?email=student@mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_400_for_student_not_enrolled(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-enrolled@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{activity_path}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student not signed up for this activity"
    }