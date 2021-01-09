import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.orm import sessionmaker, Session
from werkzeug.exceptions import Unauthorized, Forbidden

from clubelection.auth import Authenticator
from clubelection.blueprints import ballot, candidate, auth
from clubelection.committee import Committee
from clubelection.error_handlers import handle_unauthorized, handle_forbidden
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
    authenticator: Authenticator = Authenticator(session, 'secret', 'HS256')
    committee: Committee = Committee(session)

    app.register_blueprint(auth.create_blueprint(authenticator))
    app.register_blueprint(candidate.create_blueprint(session, authenticator))
    app.register_blueprint(ballot.create_blueprint(committee, authenticator))

    app.register_error_handler(Unauthorized, handle_unauthorized)
    app.register_error_handler(Forbidden, handle_forbidden)

    return app
