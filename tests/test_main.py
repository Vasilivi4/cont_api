import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure correct import of your FastAPI app

# Mock the token verification
@pytest.fixture
def client():
    return TestClient(app)

# Mocking token for test
@pytest.fixture
def token():
    return "some_token"  # This should be the mock token or a valid token used for the test

def test_limited_endpoint(client, token):
    # For testing purposes, you might want to mock or fake token validation
    # Check the response from the /limited endpoint
    response = client.get(
        "/limited", 
        headers={"Authorization": f"Bearer {token}"}  # Pass the mock token in headers
    )

    # Assert that the status code is 200 OK (assuming this is the expected response)
    assert response.status_code == 200

    # Additional checks to verify the content of the response
    assert response.json() == {"message": "This endpoint is rate limited to 5 requests per minute."}

