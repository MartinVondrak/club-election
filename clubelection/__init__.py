import os

from dotenv import load_dotenv
from flask import Flask

from clubelection.database import init_database
from clubelection.models import Candidate


def create_app():
    load_dotenv()
    session = init_database(os.getenv('DB_CONNECTION'), True)
    s = session()
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        candidate = Candidate('Martin', 'Vondrák', 'Very good candidate for managing stuff around IT.')
        s.add(candidate)
        s.commit()
        return 'Hello World {}'.format(candidate.id)

    return app
