import pytest

from app import db
from app.models import URL
from app.services import (
    create_short_url,
    generate_short_code,
    get_url_by_code,
    register_click,
)


def test_generate_short_code():
    code = generate_short_code()

    assert len(code) == 6
    assert code.isalnum()


def test_generate_short_code_custom_length():
    code = generate_short_code(10)

    assert len(code) == 10


def test_generate_short_code_invalid_length():
    with pytest.raises(ValueError):
        generate_short_code(0)


def test_create_short_url(app):
    url = create_short_url("https://example.com")

    assert url.id is not None
    assert url.original_url == "https://example.com"
    assert len(url.short_code) == 6
    assert url.clicks == 0


def test_create_short_url_invalid_address(app):
    with pytest.raises(ValueError):
        create_short_url("invalid-address")


def test_get_url_by_code(app):
    created_url = create_short_url("https://example.com")

    found_url = get_url_by_code(created_url.short_code)

    assert found_url is not None
    assert found_url.id == created_url.id


def test_get_url_by_nonexistent_code(app):
    result = get_url_by_code("NOTFOUND")

    assert result is None


def test_register_click(app):
    url = create_short_url("https://example.com")

    updated_url = register_click(url.short_code)

    assert updated_url is not None
    assert updated_url.clicks == 1


def test_register_multiple_clicks(app):
    url = create_short_url("https://example.com")

    register_click(url.short_code)
    register_click(url.short_code)
    register_click(url.short_code)

    updated_url = get_url_by_code(url.short_code)

    assert updated_url.clicks == 3


def test_register_click_nonexistent_url(app):
    result = register_click("NOTFOUND")

    assert result is None


def test_url_repr(app):
    url = URL(original_url="https://example.com", short_code="abc123")

    assert repr(url) == "<URL abc123>"


def test_create_short_url_fails_after_max_generation_attempts(app, monkeypatch):
    existing_url = URL(original_url="https://example.com", short_code="abc123")

    db.session.add(existing_url)
    db.session.commit()

    calls = []

    def generate_duplicate_code():
        calls.append(1)
        return "abc123"

    monkeypatch.setattr("app.services.generate_short_code", generate_duplicate_code)

    with pytest.raises(RuntimeError, match="Could not generate a unique short code"):
        create_short_url("https://another-example.com")

    assert len(calls) == 10
    assert URL.query.count() == 1
