"""Module for custom HTTP exceptions"""
# pylint: disable=super-init-not-called


class BadRequestError(Exception):
    """Exception for 400 Bad Request errors"""

    def __init__(self, message: str, data: dict = None):
        self.message = message
        self.data = data


class UnauthorizedError(Exception):
    """Exception for 401 Unauthorized errors"""

    def __init__(self, message: str):
        self.message = message


class NotFoundError(Exception):
    """Exception for 404 Not Found errors"""

    def __init__(self, message: str):
        self.message = message
