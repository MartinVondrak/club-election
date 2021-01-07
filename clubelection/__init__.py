import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.orm import sessionmaker, Session

from clubelection.blueprints import ballot, candidate, auth
from clubelection.committee import Committee
from clubelection.serialization import normalizer
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
    committee: Committee = Committee(session)
    app.register_blueprint(auth.create_blueprint(session))
    app.register_blueprint(candidate.create_blueprint(session))
    app.register_blueprint(ballot.create_blueprint(committee))
    return app
