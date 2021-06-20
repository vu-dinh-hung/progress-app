"""Module for error handlers"""
import traceback
import json
from flask import request
from main.utils.logger import logger


def handle_exceptions(exc):  # pylint: disable=unused-argument
    """Handle exceptions (e.g. logs them to a file) and raise a custom 500 error"""
    trace = traceback.format_exc()
    logger.error(
        "%s %s %s : 5xx INTERNAL SERVER ERROR\n%s",
        request.remote_addr,
        request.method,
        request.full_path,
        trace,
    )
    return {"message": "Something went wrong on the server end"}, 500


def handle_http_errors(exc):
    """Return JSON instead of HTML for HTTP errors"""
    response = exc.get_response()
    response.data = json.dumps({"message": exc.description})
    response.content_type = "application/json"

    return response


def handle_bad_request(exc):
    """Handle BadRequestError"""
    body = {"message": exc.message}
    if exc.data is not None:
        body["data"] = exc.data

    return body, 400


def handle_unauthorized(exc):
    """Handle UnauthorizedError"""
    return {"message": exc.message}, 401


def handle_not_found(exc):
    """Handle NotFoundError"""
    return {"message": exc.message}, 404
