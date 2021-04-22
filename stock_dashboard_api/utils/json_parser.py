import json


def get_body(request):
    """A function that executes before request,
    receive and validate json data for PUT and POST request methods.
    """
    try:
        body = json.loads(request.data)
        return body
    except (ValueError, KeyError, TypeError):
        return None
