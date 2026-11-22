from datetime import UTC, datetime

from app import db


class URL(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)

    original_url = db.Column(db.String(2048), nullable=False)

    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)

    clicks = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    def __repr__(self):
        return f"<URL {self.short_code}>"
