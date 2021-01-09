import functools
from time import time

import jwt
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import Headers
from werkzeug.exceptions import Forbidden, Unauthorized

from clubelection.models import Voter


class Authenticator:
    def __init__(self, session: Session, secret: str, algorithm: str):
        self.session: Session = session
        self.secret: str = secret
        self.algorithm: str = algorithm

    def login(self, access_code: str) -> dict:
        try:
            voter: Voter = self.session.query(Voter).filter_by(access_code=access_code).one()
        except NoResultFound:
            raise Unauthorized('Login failed.')
        return {
            'access_token': jwt.encode(
                {'voter_id': voter.id, 'exp': time() + 3600, 'access_code': access_code},
                self.secret,
                self.algorithm),
            'has_voted': voter.has_voted}

    def authenticate(self, request):
        def decorator(func):
            @functools.wraps(func)
            def wrapped_func(*args, **kwargs):
                jwt_token: str = self.get_jwt_token_from_headers(request.headers)
                token: dict = self.decode_jwt_token(jwt_token)
                is_authenticated: bool = self.authenticate_token(token)
                if not is_authenticated:
                    raise Forbidden('User not logged in.')
                return func(*args, **kwargs)

            return wrapped_func

        return decorator

    @staticmethod
    def get_jwt_token_from_headers(headers: Headers) -> str:
        header: str = headers.get('Authorization', '')
        if header.startswith('Bearer ') is False:
            return ''
        token: str = header[len('Bearer '):]
        return token

    def decode_jwt_token(self, jwt_token) -> dict:
        try:
            return jwt.decode(jwt_token, self.secret, algorithms=[self.algorithm])
        except DecodeError:
            return {}
        except ExpiredSignatureError:
            return {}

    def authenticate_token(self, token: dict) -> bool:
        if 'exp' not in token or 'voter_id' not in token or 'access_code' not in token:
            return False
        voter: Voter = self.session.query(Voter).get(token['voter_id'])
        if voter is None or token['access_code'] != voter.access_code or token['exp'] < time():
            return False
        return True
