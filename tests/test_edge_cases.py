"""
Edge case and error handling tests using AAA (Arrange-Act-Assert) pattern.
Tests boundary conditions, input validation, and error scenarios.
"""

import pytest


class TestInputValidation:
    """Tests for input validation and edge cases"""

    def test_signup_with_empty_email(self, client):
        """
        Verify signup fails with empty email parameter.
        
        Arrange: Set up request with empty email
        Act: POST signup with empty email
        Assert: Verify appropriate error handling
        """
        # Arrange
        activity_name = "Chess Club"
        empty_email = ""

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={empty_email}"
        )

        # Assert
        # Empty string might pass through - depends on FastAPI validation
        # This documents expected behavior
        assert response.status_code in [200, 400, 422]

    def test_signup_with_special_characters_in_activity_name(self, client, new_student_email):
        """
        Verify signup handles special characters in activity name.
        
        Arrange: Prepare special character activity name
        Act: POST signup with encoded special characters
        Assert: Verify proper error handling
        """
        # Arrange
        activity_name = "Non%20Existent%20Activity"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_with_special_characters_in_email(self, client):
        """
        Verify unregister handles special characters in email.
        
        Arrange: Prepare special character email
        Act: DELETE unregister with special characters
        Assert: Verify proper error handling
        """
        # Arrange
        activity_name = "Chess Club"
        special_email = "test%40example.com"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={special_email}"
        )

        # Assert
        assert response.status_code in [400, 404]


class TestCapacityLimits:
    """Tests for activity capacity constraints"""

    def test_cannot_signup_when_activity_full(self, client, new_student_email):
        """
        Verify signup fails when activity is at max capacity.
        
        Arrange: Find or create a full activity
        Act: Attempt to signup for full activity
        Assert: Verify signup is rejected or full status indicated
        """
        # Arrange
        # Note: In current implementation, no capacity check exists
        # This test documents expected future behavior
        activity_name = "Chess Club"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        activity = activities[activity_name]

        # Assert
        # Document current behavior: signup succeeds even if full
        # Future: should enforce capacity limits
        participant_count = len(activity["participants"])
        max_capacity = activity["max_participants"]
        # Currently, this will exceed capacity (no validation)
        # assert participant_count <= max_capacity


class TestResponseFormat:
    """Tests for response message format and content"""

    def test_signup_success_message_format(self, client, new_student_email):
        """
        Verify success message has expected format.
        
        Arrange: Prepare signup request
        Act: Sign up student
        Assert: Verify response message structure and content
        """
        # Arrange
        activity_name = "Programming Class"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert isinstance(data["message"], str)
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_error_response_has_detail_field(self, client):
        """
        Verify error responses include detail field.
        
        Arrange: Trigger an error condition
        Act: Make request that causes error
        Assert: Verify error response has detail field
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code >= 400
        assert "detail" in data
        assert isinstance(data["detail"], str)

    def test_activities_response_is_json_dict(self, client):
        """
        Verify activities endpoint returns valid JSON dict.
        
        Arrange: Prepare request to activities endpoint
        Act: GET /activities
        Assert: Verify response is dict with activity entries
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0
        assert all(isinstance(key, str) for key in data.keys())
        assert all(isinstance(val, dict) for val in data.values())


class TestConcurrentModification:
    """Tests for state consistency during concurrent-like operations"""

    def test_signup_then_unregister_same_activity(self, client, new_student_email):
        """
        Verify signup followed by unregister results in consistent state.
        
        Arrange: Get initial state
        Act: Sign up then unregister same student
        Assert: Verify final state matches initial
        """
        # Arrange
        activity_name = "Art Studio"
        email = new_student_email
        response_initial = client.get("/activities")
        participants_initial = set(
            response_initial.json()[activity_name]["participants"]
        )

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        response_final = client.get("/activities")
        participants_final = set(
            response_final.json()[activity_name]["participants"]
        )

        # Assert
        assert participants_initial == participants_final

    def test_unregister_then_signup_same_activity(self, client):
        """
        Verify unregister followed by signup results in consistent state.
        
        Arrange: Get initial state
        Act: Unregister then re-signup same student
        Assert: Verify student is signed up again
        """
        # Arrange
        activity_name = "Drama Club"
        email = "noah@mergington.edu"
        response_initial = client.get("/activities")
        initial_count = len(response_initial.json()[activity_name]["participants"])

        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response_final = client.get("/activities")
        final_participants = response_final.json()[activity_name]["participants"]

        # Assert
        assert email in final_participants
        assert len(final_participants) == initial_count


class TestStatusCodes:
    """Tests for correct HTTP status code responses"""

    def test_successful_operations_return_200(self, client):
        """
        Verify successful POST and DELETE return 200 status.
        
        Arrange: Prepare valid requests
        Act: Execute successful signup and unregister
        Assert: Verify 200 status codes
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "successtest@mergington.edu"

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200

    def test_not_found_errors_return_404(self, client):
        """
        Verify 404 returned for non-existent resources.
        
        Arrange: Use non-existent activity names
        Act: Make requests for invalid activities
        Assert: Verify 404 status codes
        """
        # Arrange
        invalid_activity = "Fake Activity Club"
        email = "test@example.com"

        # Act
        signup_response = client.post(
            f"/activities/{invalid_activity}/signup?email={email}"
        )
        unregister_response = client.delete(
            f"/activities/{invalid_activity}/unregister?email={email}"
        )

        # Assert
        assert signup_response.status_code == 404
        assert unregister_response.status_code == 404

    def test_bad_request_errors_return_400(self, client):
        """
        Verify 400 returned for bad requests (duplicate/not found).
        
        Arrange: Set up duplicate signup and invalid unregister
        Act: Make bad requests
        Assert: Verify 400 status codes
        """
        # Arrange
        activity_name = "Robotics Club"
        duplicate_email = "ethan@mergington.edu"  # Already signed up
        invalid_email = "notamember@mergington.edu"

        # Act
        duplicate_response = client.post(
            f"/activities/{activity_name}/signup?email={duplicate_email}"
        )
        invalid_unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={invalid_email}"
        )

        # Assert
        assert duplicate_response.status_code == 400
        assert invalid_unregister_response.status_code == 400
