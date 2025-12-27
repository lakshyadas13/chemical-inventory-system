import os

class Config:
    SECRET_KEY = "inventory-secret"

    # Use MySQL locally if DATABASE_URL is set,
    # otherwise fallback to SQLite (for Render)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///inventory.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
