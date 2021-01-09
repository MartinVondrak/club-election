from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from clubelection.auth import Authenticator
from clubelection.models import Candidate
from clubelection.serialization import normalizer


def create_blueprint(session: Session, authenticator: Authenticator) -> Blueprint:
    blueprint: Blueprint = Blueprint('candidate', __name__, url_prefix='/api')

    @blueprint.route('/candidate', methods=['GET'])
    @authenticator.authenticate(request)
    def get_candidates():
        candidates: list[Candidate] = session.query(Candidate).all()
        return jsonify(normalizer.normalize(candidates))

    return blueprint
