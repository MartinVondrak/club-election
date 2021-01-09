from werkzeug.exceptions import Unauthorized, Forbidden


def handle_unauthorized(e: Unauthorized):
    return 'Unauthorized', 401


def handle_forbidden(e: Forbidden):
    return 'Forbidden', 403
