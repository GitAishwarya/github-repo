"""
Unit tests for activities logic using AAA (Arrange-Act-Assert) pattern.
Tests business logic for activity management.
"""

import pytest


class TestActivityDataStructure:
    """Unit tests for activity data structure and validation"""

    def test_activity_has_required_fields(self, client):
        """
        Verify each activity has all required fields.
        
        Arrange: Get activities from API
        Act: Extract activity data
        Assert: Verify all required fields present
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            for field in required_fields:
                assert field in activity, f"Missing {field} in {activity_name}"

    def test_description_is_non_empty_string(self, client):
        """
        Verify description field is a non-empty string.
        
        Arrange: Get activities
        Act: Check description field type and content
        Assert: Verify description is valid string
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["description"], str)
            assert len(activity["description"]) > 0

    def test_schedule_is_non_empty_string(self, client):
        """
        Verify schedule field is a non-empty string.
        
        Arrange: Get activities
        Act: Check schedule field type and content
        Assert: Verify schedule is valid string
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["schedule"], str)
            assert len(activity["schedule"]) > 0

    def test_max_participants_is_positive_integer(self, client):
        """
        Verify max_participants is a positive integer.
        
        Arrange: Get activities
        Act: Check max_participants field type and value
        Assert: Verify max_participants is valid positive integer
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["max_participants"], int)
            assert activity["max_participants"] > 0

    def test_participants_is_list(self, client):
        """
        Verify participants field is a list.
        
        Arrange: Get activities
        Act: Check participants field type
        Assert: Verify participants is a list
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["participants"], list)

    def test_participants_contains_only_strings(self, client):
        """
        Verify all participants are email strings.
        
        Arrange: Get activities
        Act: Check each participant in the list
        Assert: Verify all participants are strings
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            for participant in activity["participants"]:
                assert isinstance(participant, str)
                assert len(participant) > 0
                assert "@" in participant  # Basic email validation


class TestParticipantLogic:
    """Unit tests for participant management logic"""

    def test_participants_count_less_than_max(self, client):
        """
        Verify participant count never exceeds max_participants.
        
        Arrange: Get activities
        Act: Count participants vs max capacity
        Assert: Verify participants <= max_participants
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            participant_count = len(activity["participants"])
            max_participants = activity["max_participants"]
            assert participant_count <= max_participants, \
                f"{activity_name} has {participant_count} participants but max is {max_participants}"

    def test_no_duplicate_participants(self, client):
        """
        Verify no duplicate emails in participant list.
        
        Arrange: Get activities
        Act: Check for duplicate participants
        Assert: Verify all participants are unique
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            participants = activity["participants"]
            assert len(participants) == len(set(participants)), \
                f"{activity_name} has duplicate participants"

    def test_signup_increases_participant_count(self, client, new_student_email):
        """
        Verify that successful signup increases participant count.
        
        Arrange: Get initial activity state
        Act: Signup new student
        Assert: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Tennis Club"
        response_before = client.get("/activities")
        activities_before = response_before.json()
        initial_count = len(activities_before[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup?email={new_student_email}")
        response_after = client.get("/activities")
        activities_after = response_after.json()
        final_count = len(activities_after[activity_name]["participants"])

        # Assert
        assert final_count == initial_count + 1
        assert new_student_email in activities_after[activity_name]["participants"]

    def test_unregister_decreases_participant_count(self, client):
        """
        Verify that unregister decreases participant count.
        
        Arrange: Get initial activity state
        Act: Unregister existing student
        Assert: Verify participant count decreased by 1
        """
        # Arrange
        activity_name = "Debate Team"
        email = "hannah@mergington.edu"
        response_before = client.get("/activities")
        activities_before = response_before.json()
        initial_count = len(activities_before[activity_name]["participants"])

        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        response_after = client.get("/activities")
        activities_after = response_after.json()
        final_count = len(activities_after[activity_name]["participants"])

        # Assert
        assert final_count == initial_count - 1
        assert email not in activities_after[activity_name]["participants"]
