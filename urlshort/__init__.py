from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.getenv('secret_key')
    from . import urlshort 
    app.register_blueprint(urlshort.bp)
    return app

