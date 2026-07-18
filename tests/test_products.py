def test_get_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product(client, auth_token):
    response = client.post(
        "/products",
        json={
            "name": "Тестовый товар",
            "description": "Описание тестового товара",
            "price": 999.99,
            "stock": 10,
            "category": "electronics"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Тестовый товар"
    assert response.json()["price"] == 999.99
    assert "id" in response.json()

def test_get_products_after_create(client, auth_token):
    # Создаём товар
    client.post(
        "/products",
        json={
            "name": "Товар для списка",
            "description": "Описание",
            "price": 500,
            "stock": 5,
            "category": "books"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    # Получаем список
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["name"] == "Товар для списка"

def test_get_product_by_id(client, auth_token):
    # Создаём товар
    create_resp = client.post(
        "/products",
        json={
            "name": "Товар по ID",
            "description": "Описание",
            "price": 300,
            "stock": 3,
            "category": "test"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    product_id = create_resp.json()["id"]
    # Получаем по ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Товар по ID"

def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.text

def test_update_product(client, auth_token):
    # Создаём товар
    create_resp = client.post(
        "/products",
        json={
            "name": "Старое имя",
            "description": "Старое описание",
            "price": 100,
            "stock": 1,
            "category": "test"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    product_id = create_resp.json()["id"]
    # Обновляем
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Новое имя",
            "price": 200
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Новое имя"
    assert response.json()["price"] == 200

def test_delete_product(client, auth_token):
    # Создаём товар
    create_resp = client.post(
        "/products",
        json={
            "name": "Товар на удаление",
            "description": "Описание",
            "price": 50,
            "stock": 1,
            "category": "test"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    product_id = create_resp.json()["id"]
    # Удаляем
    response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.text
    # Проверяем что товара нет
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404