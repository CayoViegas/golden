from app.models.order import OrderStatus, OrderType


def test_create_order_complete_flow(client):
    prod1 = client.post(
        "/products/", json={"name": "Bolinho de Charque", "price": 10.0}
    ).json()
    prod2 = client.post(
        "/products/", json={"name": "Bolinho de Queijo", "price": 5.0}
    ).json()

    order_payload = {
        "customer_name": "Abel Barros",
        "customer_phone": "11999999999",
        "customer_address": "Rua ABC, 123",
        "order_type": "immediate",
        "items": [
            {"product_id": prod1["id"], "quantity": 2},
            {"product_id": prod2["id"], "quantity": 1},
        ],
    }

    response = client.post("/orders/", json=order_payload)

    assert response.status_code == 201
    data = response.json()

    assert data["customer_name"] == "Abel Barros"
    assert data["order_type"] == OrderType.IMMEDIATE.value
    assert data["status"] == "received"

    expected_total = (10.0 * 2) + (5.0 * 1)
    assert data["total_amount"] == expected_total

    assert len(data["items"]) == 2
    assert data["items"][0]["unit_price"] == 10.0


def test_create_order_product_not_found(client):
    payload = {
        "customer_name": "Carlos Domenico",
        "customer_phone": "11999999990",
        "customer_address": "Rua BCD, 123",
        "items": [{"product_id": 9999, "quantity": 1}],
    }

    response = client.post("/orders/", json=payload)
    assert response.status_code == 404
    assert "Product ID 9999 not found" in response.json()["detail"]


def test_update_order_status(client):
    prod = client.post("/products/", json={"name": "Coquinha", "price": 2.50}).json()

    order_payload = {
        "customer_name": "Epaminondas Farias",
        "customer_phone": "11999999998",
        "customer_address": "Rua CDE, 123",
        "items": [{"product_id": prod["id"], "quantity": 1}],
    }

    order = client.post("/orders/", json=order_payload).json()
    order_id = order["id"]

    patch_payload = {"status": "preparing"}
    response = client.patch(f"/orders/{order_id}/status", json=patch_payload)

    assert response.status_code == 200
    assert response.json()["status"] == OrderStatus.PREPARING.value

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.json()["status"] == OrderStatus.PREPARING.value


def test_get_all_orders(client):
    prod = client.post(
        "/products/", json={"name": "Empada de Palmito", "price": 9.0}
    ).json()

    order_payload = {
        "customer_name": "Germano Honda",
        "customer_phone": "11999999997",
        "customer_address": "Rua EFG, 123",
        "items": [{"product_id": prod["id"], "quantity": 1}],
    }

    client.post("/orders/", json=order_payload)

    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
