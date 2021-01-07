import jwt
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from clubelection.models import Voter


def create_blueprint(session: Session) -> Blueprint:
    blueprint: Blueprint = Blueprint('auth', __name__, url_prefix='/api')

    @blueprint.route('/auth', methods=['POST'])
    def post_login():
        if 'access_code' not in request.json:
            return 'Bad request.', 400

        access_code: str = request.json['access_code']
        voter: Voter = session.query(Voter).filter_by(access_code=access_code).one()
        return jsonify({'access_token': jwt.encode({'has_votes': voter.has_voted}, access_code, 'HS256'),
                        'access_code': access_code})

    return blueprint
