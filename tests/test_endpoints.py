"""
Integration tests for FastAPI endpoints using AAA (Arrange-Act-Assert) pattern.
Tests all API routes with various scenarios.
"""

import pytest


class TestGetActivitiesEndpoint:
    """Integration tests for GET /activities endpoint"""

    def test_get_all_activities_returns_200(self, client):
        """
        Verify that GET /activities returns status 200 and activity data.
        
        Arrange: Prepare test client
        Act: Make GET request to /activities
        Assert: Verify 200 status and response contains expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Robotics Club",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]

    def test_get_activities_response_structure(self, client):
        """
        Verify response has correct data structure for each activity.
        
        Arrange: Prepare test client
        Act: Fetch activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = {
            "description": str,
            "schedule": str,
            "max_participants": int,
            "participants": list
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for field, field_type in required_fields.items():
                assert field in activity_data, f"Missing {field} in {activity_name}"
                assert isinstance(activity_data[field], field_type), \
                    f"{field} should be {field_type} in {activity_name}"


class TestRootEndpoint:
    """Integration tests for GET / endpoint"""

    def test_root_redirects_to_static(self, client):
        """
        Verify that root endpoint redirects to static index.html.
        
        Arrange: Prepare test client
        Act: Make GET request to /
        Assert: Verify 307 redirect status
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestSignupEndpoint:
    """Integration tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_success(self, client):
        """
        Verify successful signup of a new student to an activity.
        
        Arrange: Select activity and new email
        Act: POST signup request
        Assert: Verify 200 status and success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newchessstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Verify that duplicate signup returns 400 error.
        
        Arrange: Use an email already signed up for the activity
        Act: Attempt signup with duplicate email
        Assert: Verify 400 status and error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, new_student_email):
        """
        Verify that signup for non-existent activity returns 404.
        
        Arrange: Use a non-existent activity name
        Act: Attempt signup for invalid activity
        Assert: Verify 404 status and error detail
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestUnregisterEndpoint:
    """Integration tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_existing_student_success(self, client):
        """
        Verify successful unregister of an existing student.
        
        Arrange: Select activity and student already signed up
        Act: DELETE unregister request
        Assert: Verify 200 status and success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_nonexistent_student_returns_400(self, client):
        """
        Verify that unregister of non-existent participant returns 400.
        
        Arrange: Use an email not signed up for the activity
        Act: Attempt unregister for non-participant
        Assert: Verify 400 status and error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notamember@mergington.edu"  # Not signed up for this activity

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """
        Verify that unregister from non-existent activity returns 404.
        
        Arrange: Use a non-existent activity name
        Act: Attempt unregister from invalid activity
        Assert: Verify 404 status and error detail
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
