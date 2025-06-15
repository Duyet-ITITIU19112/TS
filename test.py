import os
from flask import Flask
from flask_session import Session
from src.models import db
from src.config.dev_config import DevConfig
from src.services.elastic_service import create_index_if_not_exists
from src.routes.auth import auth_bp
from src.routes.search import search_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    # Enable server-side sessions (filesystem)
    app.config.setdefault("SESSION_TYPE", "filesystem")
    Session(app)

    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)

    return app


def main():
    print("ENV VAR: MS_REDIRECT_URI =", os.getenv("MS_REDIRECT_URI"))

    app = create_app()
    with app.app_context():
        # Initialize tables and Elasticsearch index
        db.create_all()
        create_index_if_not_exists()
        print("✅ Database and ES initialized")

    # Start development server
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
