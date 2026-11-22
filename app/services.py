
import secrets
import string

from sqlalchemy.exc import IntegrityError

from app import db
from app.models import URL
from app.validators import is_valid_url, is_valid_short_code


CHARACTERS = string.ascii_letters + string.digits
MAX_GENERATION_ATTEMPTS = 10


def generate_short_code(length=6):
    return "".join(
        secrets.choice(CHARACTERS)
        for _ in range(length)
    )


def create_short_url(original_url, custom_code=None):
    if not is_valid_url(original_url):
        raise ValueError("Podany adres URL jest nieprawidłowy.")

    original_url = original_url.strip()

    # Własny kod użytkownika
    if custom_code and custom_code.strip():
        custom_code = custom_code.strip().lower()

        if not is_valid_short_code(custom_code):
            raise ValueError(
                "Własny kod musi mieć od 3 do 10 znaków "
                "i może zawierać tylko litery, cyfry oraz myślniki."
            )

        existing_url = URL.query.filter_by(
            short_code=custom_code
        ).first()

        if existing_url:
            raise ValueError(
                "Ten kod jest już zajęty. Wybierz inny."
            )

        url = URL(
            original_url=original_url,
            short_code=custom_code
        )

        db.session.add(url)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            raise ValueError(
                "Ten kod jest już zajęty. Wybierz inny."
            )

        return url

    # Automatyczne generowanie kodu
    for _ in range(MAX_GENERATION_ATTEMPTS):
        short_code = generate_short_code()

        url = URL(
            original_url=original_url,
            short_code=short_code
        )

        db.session.add(url)

        try:
            db.session.commit()
            return url

        except IntegrityError:
            db.session.rollback()

    raise RuntimeError(
        "Could not generate a unique short code."
    )


def get_url_by_code(short_code):
    return URL.query.filter_by(
        short_code=short_code
    ).first()


def register_click(short_code):
    url = get_url_by_code(short_code)

    if url is None:
        return None

    url.clicks += 1
    db.session.commit()

    return url
