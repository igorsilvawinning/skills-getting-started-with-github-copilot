from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_participant_removes_student_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    try:
        activities[activity_name]["participants"].append(email)

        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
    finally:
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)
