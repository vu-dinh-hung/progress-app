"""Module for error handlers"""
import traceback
from flask import request
from main.utils.logger import logger


def handle_exceptions(exc):
    """Handles exceptions (e.g. logs them to a file) and raise a custom 500 error"""
    trace = traceback.format_exc()
    logger.error(
        "%s %s %s : 5xx INTERNAL SERVER ERROR\n%s",  # pylint: disable=line-too-long
        request.remote_addr,
        request.method,
        request.full_path,
        trace,
    )
    return {"message": "Something went wrong on the server end"}, 500
