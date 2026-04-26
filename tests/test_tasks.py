import pytest


@pytest.fixture
def user_created(client):
    payload = {
        "name": "Juan Perez",
        "email": "juanito@gmail.com",
        "age": 35
    }

    response = client.post("/users/", json=payload)
    return response.json()

def test_create_task(client, user_created):
    user_id = user_created["id"]
    payload = {
        "title": "Task 1",
        "description": "This is the first task",
        "completed": False
    }
    response = client.post(f"/users/{user_id}/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Task 1"
    assert data["description"] == "This is the first task"
    assert data["completed"] == False
    assert "id" in data

def test_get_tasks(client, user_created):
    user_id = user_created["id"]
    payload = {
        "title": "Task 1",
        "description": "This is the first task",
        "completed": False
    }
    client.post(f"/users/{user_id}/tasks/", json=payload)

    response = client.get(f"/users/{user_id}/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"
    assert data[0]["description"] == "This is the first task"
    assert data[0]["completed"] == False
    assert "id" in data[0]

def test_task_update(client, user_created):
    user_id = user_created["id"]
    payload = {
        "title": "programing task",
        "description": "programing test",
        "completed": False
    }
    response = client.post(f"/users/{user_id}/tasks/", json=payload)
    task_id = response.json()["id"]
    payload_update = {
        "title": "programing task updated",
        "description": "programing test updated",
    }
    response = client.patch(f"/users/{user_id}/tasks/{task_id}", json=payload_update)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "programing task updated"
    assert data["description"] == "programing test updated"
    assert data["completed"] == False

def test_filter_task_completed(client, user_created):
    user_id = user_created["id"]
    payload1 = {
        "title": "Task 1",
        "description": "This is the first task",
        "completed": False
    }

    payload2 = {
        "title": "Task 2",
        "description": "This is the second task",
        "completed": True
    }
    client.post(f"/users/{user_id}/tasks/", json=payload1)
    client.post(f"/users/{user_id}/tasks/", json=payload2)

    response = client.get(f"/users/{user_id}/tasks/?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"
    assert data[0]["description"] == "This is the second task"
    assert data[0]["completed"] == True


def test_delete_task(client, user_created):
    user_id = user_created["id"]
    payload = {
        "title": "Task to delete",
        "description": "This task will be deleted",
        "completed": False
    }
    response = client.post(f"/users/{user_id}/tasks/", json=payload)
    task_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}/tasks/{task_id}")
    assert response.status_code == 404
