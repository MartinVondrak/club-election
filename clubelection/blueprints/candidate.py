from flask import Blueprint, jsonify
from sqlalchemy.orm import Session

from clubelection.models import Candidate
from clubelection.serialization import normalizer


def create_blueprint(session: Session) -> Blueprint:
    blueprint: Blueprint = Blueprint('candidate', __name__, url_prefix='/api')

    @blueprint.route('/candidate', methods=['GET'])
    def get_candidates():
        candidates: list[Candidate] = session.query(Candidate).all()
        return jsonify(normalizer.normalize(candidates))

    return blueprint
