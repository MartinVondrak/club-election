import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker, Session

from clubelection.normalizer import normalizer
from clubelection.database import init_database
from clubelection.models import Candidate


def create_app() -> Flask:
    load_dotenv()
    app: Flask = Flask(__name__)
    db_connection_string: Optional[str] = os.getenv('DB_CONNECTION')

    if db_connection_string is None:
        raise Exception()

    session_maker: sessionmaker = init_database(db_connection_string, app.debug)
    session: Session = session_maker()

    @app.route('/hello')
    def hello():
        candidate = Candidate('Martin', 'Vondrák',
                              'Very good candidate for managing stuff around IT.')
        session.add(candidate)
        session.commit()
        return 'Hello World {}'.format(candidate.id)

    @app.route('/candidates')
    def get_candidates():
        candidates: list[Candidate] = session.query(Candidate).all()
        return jsonify(normalizer.normalize(candidates))

    return app
