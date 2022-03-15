from functools import wraps
import json


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class ErrorResponse(object):
    def __init__(self, code: str, message: str, details=None) -> None:
        self.code = code
        self.message = message
        self.details = details


def meroxa_api_response(*args, **kwargs):

    async def wrapper(func):
        res = await func(*args, **kwargs)

        try:
            return await kwargs['return_type'](**json.loads(res))
        except:
            return ErrorResponse(**json.loads(res))

    print(args, kwargs)
    return wrapper
