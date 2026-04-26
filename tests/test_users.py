
def list_empty_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["age"] == user_data["age"]
    assert "id" in data
    assert data["tasks"] == []

def test_get_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }
    client.post("/users/", json=user_data)

    response = client.get("/users/1")
    assert response.status_code == 200

def test_duplicate_email(client):
    user_data = {
        "name": "maria",
        "email": "maria@example.com",
        "age": 25
    }

    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)

    assert response.status_code == 400

def test_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_update_user(client):
    user_data = {
        "name": "Alice",
        "email": "alice@gmail.com",
        "age": 28
    }
    client.post("/users/", json=user_data)

    user_data_update = {
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "age": 29
    }
    response = client.patch("/users/1", json=user_data_update)
    assert response.status_code == 200


def test_delete_user(client):
    user_data = {
        "name": "Bob",
        "email": "bob@example.com",
        "age": 35
    }
    client.post("/users/", json=user_data)

    response = client.delete("/users/1")
    assert response.status_code == 204

    response = client.get("/users/1")
    assert response.status_code == 404