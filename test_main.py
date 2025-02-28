import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importing FastAPI app

client = TestClient(app)

# Test fetching users
@pytest.mark.parametrize("page, limit", [(1, 2), (2, 5)])
def test_get_users(page, limit):
    response = client.get(f"/v1/users?page={page}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test creating a new user
def test_create_user():
    new_user = {"name": "John Doe", "email": "johndoe@example.com", "is_active": True, "gender": "male"}
    response = client.post("/v1/users", json=new_user)
    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["email"] == "johndoe@example.com"

# Test full update of a user
def test_update_user_full():
    user_id = "valid_user_id_here"  # Replace with a real user ID from your database
    updated_user = {"name": "Updated Name", "email": "updated@example.com", "is_active": False, "gender": "female"}
    response = client.put(f"/v1/users/{user_id}", json=updated_user)
    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["name"] == "Updated Name"

# Test partial update of a user
def test_update_user_partial():
    user_id = "valid_user_id_here"  # Replace with a real user ID from your database
    update_data = {"name": "Partially Updated"}
    response = client.patch(f"/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "Partially Updated"

# Test deleting a user
def test_delete_user():
    user_id = "valid_user_id_here"  # Replace with a real user ID from your database
    response = client.delete(f"/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
