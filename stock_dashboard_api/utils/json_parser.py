import json


def middleware_body_parse_json(request):
    """A function that executes before request,
    receive and validate json data for PUT and POST request methods.
    """
    try:
        request.body = json.loads(request.data)
        return request
    except (ValueError, KeyError, TypeError):
        pass
