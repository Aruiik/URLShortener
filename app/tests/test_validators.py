import pytest

from app.validators import is_valid_url


@pytest.mark.parametrize(
    "url",
    [
        "https://google.com",
        "http://example.com",
        "https://github.com/user/repository",
        "https://example.com/article?id=123",
        "http://localhost:5000",
    ],
)
def test_valid_urls(url):
    assert is_valid_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "",
        " ",
        "example.com",
        "ftp://example.com",
        "javascript:alert(1)",
        "https://",
        "http://",
        "https://example.com:invalid",
    ],
)
def test_invalid_urls(url):
    assert is_valid_url(url) is False


def test_url_with_whitespace():
    assert is_valid_url("  https://example.com  ") is True


def test_non_string_url():
    assert is_valid_url(None) is False
