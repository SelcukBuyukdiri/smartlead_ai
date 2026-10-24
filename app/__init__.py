from flask import Flask
from flask_cors import CORS
from config import Config
from app import database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS ayarı (calismaFlask.py'deki gibi tüm kaynaklara açık)
    CORS(app)

    # Veritabanını başlat
    with app.app_context():
        database.init_db(app)

    # Rotaları kaydet
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
