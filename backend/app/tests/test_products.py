def test_create_product(client):
    payload = {
        "name": "Mini Coxinha de Frango",
        "description": "Mini Coxinha de Frango",
        "price": 22,
        "is_active": True    
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data
    assert data["id"] is not None

def test_read_product(client):
    payload = {
        "name": "Bolinho de Charque",
        "price": 31
    }
    client.post("/products/", json=payload)

    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Bolinho de Charque"

def test_read_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404

def test_update_product(client):
    payload = {
        "name": "Mini Churros",
        "price": 44
    }
    response = client.post("/products/", json=payload)
    product_id = response.json()["id"]

    update_payload = {
        "name": "Coxinha de Calabresa",
        "price": 33
    }
    response = client.patch(f"/products/{product_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Coxinha de Calabresa"
    assert data["price"] == 33

    get_response = client.get(f"/products/{product_id}")
    assert get_response.json()["name"] == "Coxinha de Calabresa"

def test_update_product_not_found(client):
    response = client.patch("/products/999", json={"name": "Nada"})
    assert response.status_code == 404

def test_delete_product(client):
    payload = {
        "name": "Empada de Frango",
        "price": 7
    }
    response = client.post("/products/", json=payload)
    product_id = response.json()["id"]

    del_response = client.delete(f"/products/{product_id}")
    assert del_response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404