"""
Pytest configuration and shared fixtures for API tests.
Provides test client and sample data fixtures using AAA pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


# Store the original activities state
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and intramural games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu", "james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis instruction and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media techniques",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "lily@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and stage acting workshops",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 14,
        "participants": ["ethan@mergington.edu", "logan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Public speaking and competitive debate",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["hannah@mergington.edu", "alexander@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient instance for making API requests.
    
    This fixture is used in the Arrange phase to set up the test environment.
    Automatically resets app state between tests for proper isolation.
    """
    # Arrange: Reset app state to original before each test
    app_module.activities.clear()
    app_module.activities.update(ORIGINAL_ACTIVITIES)
    
    # Act: Create and return test client
    return TestClient(app_module.app)


@pytest.fixture
def sample_activities():
    """
    Fixture: Returns sample activity data for testing.
    
    Used in the Arrange phase to prepare test data.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture
def test_email():
    """
    Fixture: Provides a test email for signup scenarios.
    
    Used in the Arrange phase to set up test data.
    """
    return "testuser@mergington.edu"


@pytest.fixture
def new_student_email():
    """
    Fixture: Provides a unique email for a new student signup.
    
    Used in the Arrange phase to simulate new registrations.
    """
    return "newstudent@mergington.edu"
