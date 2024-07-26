from fastapi.testclient import TestClient


def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/items")
    assert response.status_code == 200
    items = response.json()

    assert len(items) == 2


def test_find_by_id_正常系(client_fixture: TestClient):
    response = client_fixture.get("/items/1")
    assert response.status_code == 200
    item = response.json()

    assert item["id"] == 1
    assert item["name"] == "item1"


def test_find_by_id_異常系(client_fixture: TestClient):
    response = client_fixture.get("/items/999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Item not found"


def test_find_by_name_正常系(client_fixture: TestClient):
    response = client_fixture.get("/items/?name=item1")
    assert response.status_code == 200
    item = response.json()
    assert len(item) == 1
    assert item[0]["id"] == 1
    assert item[0]["name"] == "item1"


def test_create_正常系(client_fixture: TestClient):
    response = client_fixture.post(
        "/items", json={"name": "item3", "price": 30000, "user_id": 1}
    )
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "item3"

    get_response = client_fixture.get("/items")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 3


# def test_create_異常系(client_fixture: TestClient):
#     response = client_fixture.post(
#         "/items", json={"name": "item3", "price": 30000, "user_id": 999}
#     )
#     assert response.status_code == 401
#     error = response.json()
#     assert error["detail"] == "User not found"


def test_update_正常系(client_fixture: TestClient):
    response = client_fixture.put(
        "/items/1", json={"name": "item1_updated", "price": 30000, "user_id": 1}
    )

    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "item1_updated"
    assert item["price"] == 30000


def test_update_異常系(client_fixture: TestClient):
    response = client_fixture.put(
        "/items/999", json={"name": "item1_updated", "price": 30000, "user_id": 1}
    )

    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Item not found"


def test_delete_正常系(client_fixture: TestClient):
    response = client_fixture.delete("/items/1")
    assert response.status_code == 200

    get_response = client_fixture.get("/items")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1


def test_delete_異常系(client_fixture: TestClient):
    response = client_fixture.delete("/items/999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Item not found"
