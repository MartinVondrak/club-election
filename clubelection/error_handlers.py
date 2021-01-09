from werkzeug.exceptions import Unauthorized, Forbidden


def handle_unauthorized(e: Unauthorized):
    return 'Unauthorized', 401


def handle_forbidden(e: Forbidden):
    return 'Forbidden', 403


def handle_exception(e: Exception):
    print(e)
    return 'Internal Server Error', 500
