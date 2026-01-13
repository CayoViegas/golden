from faker import Faker

from app.models.order import OrderStatus, OrderType

fake = Faker("pt_BR")


def test_create_order_complete_flow(client):
    price1 = float(fake.random_number(digits=2))
    price2 = float(fake.random_number(digits=2))

    prod1 = client.post(
        "/products/", json={"name": fake.word(), "price": price1}
    ).json()
    prod2 = client.post(
        "/products/", json={"name": fake.word(), "price": price2}
    ).json()

    customer_name = fake.name()
    order_payload = {
        "customer_name": customer_name,
        "customer_phone": fake.phone_number(),
        "customer_address": fake.address(),
        "order_type": "immediate",
        "items": [
            {"product_id": prod1["id"], "quantity": 2},
            {"product_id": prod2["id"], "quantity": 1},
        ],
    }

    response = client.post("/orders/", json=order_payload)

    assert response.status_code == 201
    data = response.json()

    assert data["customer_name"] == customer_name
    assert data["order_type"] == OrderType.IMMEDIATE.value
    assert data["status"] == OrderStatus.RECEIVED.value

    expected_total = (price1 * 2) + (price2 * 1)
    assert data["total_amount"] == expected_total


def test_read_order_not_found(client):
    response = client.get("/orders/9999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]


def test_create_order_product_not_found(client):
    payload = {
        "customer_name": fake.name(),
        "customer_phone": fake.phone_number(),
        "customer_address": fake.address(),
        "items": [{"product_id": 9999, "quantity": 1}],
    }

    response = client.post("/orders/", json=payload)
    assert response.status_code == 404
    assert "Product ID" in response.json()["detail"]


def test_update_order_status(client):
    prod = client.post("/products/", json={"name": "Coquinha", "price": 2.50}).json()

    order_payload = {
        "customer_name": fake.name(),
        "customer_phone": fake.phone_number(),
        "customer_address": fake.address(),
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


def test_update_order_status_not_found(client):
    patch_payload = {"status": "preparing"}
    response = client.patch("/orders/99999/status", json=patch_payload)
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]


def test_get_all_orders(client):
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
