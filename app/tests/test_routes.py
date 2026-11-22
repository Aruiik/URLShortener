from app.services import create_short_url


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "ShortLink" in response.get_data(as_text=True)


def test_dashboard_page(client):
    response = client.get("/dashboard")

    assert response.status_code == 200


def test_create_short_url(client):
    response = client.post(
        "/", data={"original_url": "https://example.com"}, follow_redirects=True
    )

    assert response.status_code == 200
    assert "Link został pomyślnie skrócony!" in response.get_data(as_text=True)


def test_create_short_url_invalid(client):
    response = client.post(
        "/", data={"original_url": "invalid-url"}, follow_redirects=True
    )

    assert response.status_code == 200
    assert "Invalid URL address." in response.get_data(as_text=True)


def test_redirect_to_original_url(client, app):
    with app.app_context():
        url = create_short_url("https://example.com")
        short_code = url.short_code

    response = client.get(f"/{short_code}")

    assert response.status_code == 302
    assert response.location == "https://example.com"


def test_redirect_increases_click_counter(client, app):
    with app.app_context():
        url = create_short_url("https://example.com")
        short_code = url.short_code

    client.get(f"/{short_code}")

    with app.app_context():
        from app.services import get_url_by_code

        updated_url = get_url_by_code(short_code)

        assert updated_url.clicks == 1


def test_nonexistent_short_code(client):
    response = client.get("/NOTFOUND")

    assert response.status_code == 404


def test_dashboard_displays_created_link(client):
    client.post(
        "/", data={"original_url": "https://example.com"}, follow_redirects=True
    )

    response = client.get("/dashboard")

    assert response.status_code == 200

    page = response.get_data(as_text=True)

    assert "example.com" in page


def test_delete_url(client, app):
    with app.app_context():
        url = create_short_url("https://example.com")
        url_id = url.id

    response = client.post(f"/delete/{url_id}", follow_redirects=True)

    assert response.status_code == 200
    assert "Link został usunięty." in response.get_data(as_text=True)


def test_delete_nonexistent_url(client):
    response = client.post("/delete/9999")

    assert response.status_code == 404
