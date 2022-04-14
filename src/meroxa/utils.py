import json

from .types import MeroxaApiResponse


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "reprJSON"):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class ErrorResponse(object):
    def __init__(self, code: str, message: str, details=None) -> None:
        self.code = code
        self.message = message
        self.details = details


def parseErrorMessage(error):
    try:
        return ErrorResponse(**json.loads(error))
    except BaseException:
        split = error.split("\n", 1)
        return ErrorResponse("Error", split[0])


def api_response(return_type: MeroxaApiResponse):
    """Meroxa API Response function decorator

    Takes the response from a function that returns a
    `aiohttp.ClientResponse.text()` and parses the response
    into a `MeroxaApi` object. Returns an ErrorResponse if the
    message cannot be parsed

    :param return_type object of type MeroxaApiResponse
    :rtype: (ErrorResponse, MeroxaApiResponse)
    """

    def mid(func):
        async def wrapper(*args, **kwargs):
            res = await func(*args, **kwargs)
            try:
                parsed = json.loads(res)
                if isinstance(parsed, list):
                    return (None, [return_type(**par) for par in parsed])
                return (None, return_type(**json.loads(res)))
            except BaseException:
                return (parseErrorMessage(res), None)

        return wrapper

    return mid
