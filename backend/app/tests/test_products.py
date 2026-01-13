from faker import Faker

from app.models.product import Product

fake = Faker("pt_BR")


def test_product_repr():
    prod = Product(name="Test", price=10.0)

    assert repr(prod) == "<Product(name=Test)>"


def test_create_product(client):
    payload = {
        "name": fake.food_name() if hasattr(fake, "food_name") else fake.word(),
        "description": fake.sentence(),
        "price": float(fake.random_number(digits=2)),
        "is_active": True,
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data
    assert data["id"] is not None


def test_read_product(client):
    name = fake.word()
    payload = {"name": name, "price": 10.50}
    client.post("/products/", json=payload)

    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    names = [p["name"] for p in data]
    assert name in names


def test_read_product_by_id(client):
    name = fake.word()
    payload = {"name": name, "price": 10.50}
    response = client.post("/products/", json=payload)
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name


def test_read_product_not_found(client):
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_update_product(client):
    initial_price = float(fake.random_number(digits=2))
    payload = {"name": fake.word(), "price": initial_price}
    create_res = client.post("/products/", json=payload)
    product_id = create_res.json()["id"]

    new_name = fake.word()
    update_payload = {"name": new_name, "price": initial_price + 10}
    response = client.patch(f"/products/{product_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name
    assert data["price"] == initial_price + 10


def test_update_product_not_found(client):
    response = client.patch("/products/999", json={"name": "Nada"})
    assert response.status_code == 404


def test_delete_product(client):
    payload = {"name": fake.word(), "price": 7}
    response = client.post("/products/", json=payload)
    product_id = response.json()["id"]

    del_response = client.delete(f"/products/{product_id}")
    assert del_response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404
