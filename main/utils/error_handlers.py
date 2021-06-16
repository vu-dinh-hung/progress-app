import traceback
from flask import request
from main.utils.logger import logger


def handle_exceptions(e):
    tb = traceback.format_exc()
    logger.error(
        f'{request.remote_addr} {request.method} {request.full_path} : 5xx INTERNAL SERVER ERROR\n{tb}'
    )
    return {'message': 'Something went wrong on the server end'}, 500
