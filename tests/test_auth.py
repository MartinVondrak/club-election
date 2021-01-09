from time import time

import jwt
import pytest
from flexmock import flexmock
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import Headers
from werkzeug.exceptions import Unauthorized

from clubelection.auth import Authenticator
from clubelection.models import Voter


def test_should_login():
    voter: Voter = Voter('existing_access_code', False)
    voter.id = 1
    query_mock = flexmock()
    query_mock.should_receive('one').and_return(voter).once()
    query_mock.should_receive('filter_by').with_args(access_code='existing_access_code').and_return(query_mock).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    authenticator: Authenticator = Authenticator(session_mock, 'test', 'HS256')
    token: dict = authenticator.login('existing_access_code')
    assert token['has_voted'] is False
    access_token: dict = jwt.decode(token['access_token'], 'test', algorithms=['HS256'])
    assert access_token['voter_id'] == 1
    assert access_token['access_code'] == 'existing_access_code'
    assert access_token['exp'] > time()


def test_should_not_login_and_raise_error_if_voter_not_found():
    query_mock = flexmock()
    query_mock.should_receive('one').and_raise(NoResultFound).once()
    query_mock.should_receive('filter_by').with_args(access_code='non_existing_access_code').and_return(
        query_mock).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    authenticator: Authenticator = Authenticator(session_mock, 'test', 'HS256')
    with pytest.raises(Unauthorized):
        authenticator.login('non_existing_access_code')


@pytest.mark.parametrize(['headers', 'result'],
                         [(Headers({'Authorization': 'Bearer jwt_token'}), 'jwt_token'),
                          (Headers({'Authorization': 'JWT token'}), ''), (Headers(), '')])
def test_should_get_jwt_token_from_headers(headers, result):
    token: str = Authenticator.get_jwt_token_from_headers(headers)
    assert token == result


def test_should_authenticate_token():
    token: dict = {'voter_id': 1, 'exp': time() + 3600, 'access_code': 'code'}
    voter: Voter = Voter('code', False)
    voter.id = 1
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(token['voter_id']).and_return(voter).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    authenticator: Authenticator = Authenticator(session_mock, 'test', 'HS256')
    is_authenticated: bool = authenticator.authenticate_token(token)
    assert is_authenticated is True


@pytest.mark.parametrize('token', ({'exp': time() + 3600, 'access_code': 'code'}, {'access_code': 'code'},
                                   {'voter_id': 1, 'exp': time() + 3600}, {'voter_id': 1},
                                   {'voter_id': 3600, 'access_code': 'code'}))
def test_should_not_authenticate_token_if_invalid_format_of_token(token: dict):
    authenticator: Authenticator = Authenticator(flexmock(Session()), 'test', 'HS256')
    is_authenticated: bool = authenticator.authenticate_token(token)
    assert is_authenticated is False


@pytest.mark.parametrize('token', ({'voter_id': 1, 'exp': time() - 3600, 'access_code': 'code'},
                                   {'voter_id': 1, 'exp': time() + 3600, 'access_code': 'invalid'}))
def test_should_not_authenticate_token_if_invalid_token(token: dict):
    voter: Voter = Voter('code', False)
    voter.id = 1
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(token['voter_id']).and_return(voter).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    authenticator: Authenticator = Authenticator(session_mock, 'test', 'HS256')
    is_authenticated: bool = authenticator.authenticate_token(token)
    assert is_authenticated is False


def test_should_not_authenticate_token_if_voter_not_found():
    token: dict = {'voter_id': 10, 'exp': time() + 3600, 'access_code': 'code'}
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(token['voter_id']).and_return(None).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    authenticator: Authenticator = Authenticator(session_mock, 'test', 'HS256')
    is_authenticated: bool = authenticator.authenticate_token(token)
    assert is_authenticated is False


valid_decoded_token: dict = {'voter_id': 1, 'exp': time() + 3600, 'access_code': 'code'}


@pytest.mark.parametrize(['token', 'result'],
                         [('', {}),
                          (jwt.encode({'voter_id': 1, 'exp': 1234, 'access_code': 'code'}, 'test', 'HS256'), {}),
                          (jwt.encode(valid_decoded_token, 'test', 'HS256'), valid_decoded_token)])
def test_should_decode_jwt_token(token: str, result: dict):
    authenticator: Authenticator = Authenticator(flexmock(Session()), 'test', 'HS256')
    assert authenticator.decode_jwt_token(token) == result
