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


def api_response(return_type):
    def mid(func):
        async def wrapper(*args, **kwargs):
            res = await func(*args, **kwargs)
            try:
                parsed = json.loads(res)
                if isinstance(parsed, list):
                    return [return_type(**par) for par in parsed]
                return return_type(**json.loads(res))
            except:
                # Some errors don't have newlines in them...
                split = res.split('\n', 1)
                return ErrorResponse(**json.loads(split[-1]))
        return wrapper
    return mid
