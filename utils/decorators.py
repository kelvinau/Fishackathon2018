from settings import INTERNAL_SERVER_API_KEY
from src.user.models import UserSession
from utils.constants import USER_TOKEN, API_KEY
from utils.exceptions import MissingParameter
from utils.general import dict_require_params

USER_KWARG_KEY = 'user_account'


def require_parameters(required_params):
    def decorator(func):
        def inner(handler, *args, **kwargs):
            try:
                required_params_values = dict_require_params(handler.request, required_params)
                kwargs.update(required_params_values)
            except MissingParameter as e:
                return handler.response_parameter_missing(e)
            return func(handler, *args, **kwargs)

        return inner

    return decorator


def require_logged_in_user(func):
    @require_api_key
    @require_parameters((USER_TOKEN,))
    def inner(handler, *args, **kwargs):
        user_account = UserSession.get_logged_in_user_by_token(token=kwargs[USER_TOKEN])
        if user_account:
            kwargs[USER_KWARG_KEY] = user_account
        else:
            return handler.response_permission_denied("Permission Denied")
        return func(handler, *args, **kwargs)

    return inner


def require_api_key(func):
    @require_parameters((API_KEY,))
    def inner(handler, *args, **kwargs):
        if kwargs[API_KEY] != INTERNAL_SERVER_API_KEY:
            return handler.response_permission_denied("Permission Denied")
        return func(handler, *args, **kwargs)

    return inner
