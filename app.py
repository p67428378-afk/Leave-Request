from flask import Flask
from models import db
from config import DevelopmentConfig, TestingConfig
import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    if os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(config_class)

    db.init_app(app)

    from routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
