import functools
import json
import logging

import discord
import grpc


logger = logging.getLogger(__name__)


def handle_discord_exceptions(Response):
    """converts discord HTTP exceptions into gRPC context"""

    _CODES_MAPPING = {
        400: grpc.StatusCode.INVALID_ARGUMENT,
        401: grpc.StatusCode.UNAUTHENTICATED,
        403: grpc.StatusCode.PERMISSION_DENIED,
        404: grpc.StatusCode.NOT_FOUND,
        405: grpc.StatusCode.INVALID_ARGUMENT,
        429: grpc.StatusCode.RESOURCE_EXHAUSTED,
        500: grpc.StatusCode.INTERNAL,
        502: grpc.StatusCode.UNAVAILABLE,
        504: grpc.StatusCode.DEADLINE_EXCEEDED,
    }

    def wrapper(func):
        @functools.wraps(func)
        async def decorated(self, request, context):
            try:
                return await func(self, request, context)
            except discord.errors.HTTPException as ex:
                logger.info(
                    "%s: Discord HTTP exception: %s:\n%s",
                    func.__name__,
                    ex,
                    request,
                )
                details = _gen_grpc_error_details(
                    status=ex.status, code=ex.code, text=ex.text
                )
                context.set_code(_CODES_MAPPING.get(ex.status, grpc.StatusCode.UNKNOWN))
                context.set_details(json.dumps(details))
                return Response()
            except Exception as ex:
                logger.warning(
                    "%s: Unexpected exception: %s:\n%s",
                    func.__name__,
                    ex,
                    request,
                )
                return Response()

        return decorated

    return wrapper


def _gen_grpc_error_details(status: int, code: int, text: str):
    return {
        "type": "HTTPException",
        "status": int(status),
        "code": int(code),
        "text": str(text),
    }


def log_request(func):
    """Logs every request"""

    async def decorated(self, request, context):
        logger.debug("Received request: %s\n%s", func.__name__, request)
        return await func(self, request, context)

    return decorated
