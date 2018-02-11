import json

from utils.exceptions import MissingParameter


def get_param(request, param):
    param_value = None

    json_data = None
    if hasattr(request, 'body'):
        try:
            json_data = json.loads(request.body)
        except ValueError:
            pass

    # get the value from both get and post params
    if request.get(param) is not None and request.get(param) != '':
        param_value = request.get(param)
    elif json_data:
        param_value = json_data.get(param)
    return param_value


def dict_require_params(request, params):
    res_dict = {}
    for param in params:
        param_value = get_param(request, param)
        if param_value is None:
            raise MissingParameter(param)

        res_dict[param] = param_value
    return res_dict
