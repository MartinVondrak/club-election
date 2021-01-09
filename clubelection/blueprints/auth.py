from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized

from clubelection.auth import Authenticator


def create_blueprint(authenticator: Authenticator) -> Blueprint:
    blueprint: Blueprint = Blueprint('auth', __name__, url_prefix='/api')

    @blueprint.route('/auth', methods=['POST'])
    def login():
        if 'access_code' not in request.json:
            raise Unauthorized('Missing credentials')

        token: dict = authenticator.login(request.json['access_code'])
        return jsonify(token)

    return blueprint
