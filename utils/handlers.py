import json

import webapp2
from webapp2_extras import sessions, jinja2


STATUS_SUCCESS = 1
STATUS_FAIL = 0
KEY_STATUS = 'status'
KEY_DATA = 'data'
KEY_MESSAGE = 'message'
KEY_PARAMETER_MISSING = 'Missing parameter'

RESPONSE_STATUS_SUCCESS_CODE = 200
RESPONSE_STATUS_BAD_REQUEST_CODE = 400
RESPONSE_STATUS_PERMISSION_DENIED_CODE = 403

MESSAGE_PERMISSION_DENIED = 'Unauthorized request'
MESSAGE_PARAMETERS_MISSING = 'Parameters are missing'


class Response(object):
    response_code = RESPONSE_STATUS_SUCCESS_CODE
    status = STATUS_SUCCESS
    message = ""
    data = {}

    def __init__(self, response):
        self.response = response

    def respond_success(self, message="", data={}):
        self.status = STATUS_SUCCESS
        self.message = message
        self.data = data
        self.response_code = RESPONSE_STATUS_SUCCESS_CODE

        return self.respond()

    def respond_failure(self, message="", data={}):
        self.status = STATUS_FAIL
        self.message = message
        self.data = data
        self.response_code = RESPONSE_STATUS_BAD_REQUEST_CODE

        return self.respond()

    def respond_parameters_missing(self, parameter):
        self.status = STATUS_FAIL
        self.message = MESSAGE_PARAMETERS_MISSING
        self.data = {KEY_PARAMETER_MISSING: str(parameter)}
        self.response_code = RESPONSE_STATUS_BAD_REQUEST_CODE

        return self.respond()

    def respond_permission_denied(self, message=MESSAGE_PERMISSION_DENIED):
        self.status = STATUS_FAIL
        self.message = message
        self.response_code = RESPONSE_STATUS_PERMISSION_DENIED_CODE

        return self.respond()

    def respond(self):
        response_data_dict = {KEY_STATUS: self.status, KEY_MESSAGE: self.message, KEY_DATA: self.data}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(self.response_code)
        self.response.out.write(json.dumps(response_data_dict))


class BaseHandler(webapp2.RequestHandler):

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def dispatch(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def response_success(self, message='', data={}):
        Response(self.response).respond_success(message=message, data=data)

    def response_failure(self, message='', data={}):
        Response(self.response).respond_failure(message=message, data=data)

    def response_permission_denied(self, message=''):
        Response(self.response).respond_permission_denied(message=message)

    def response_parameter_missing(self, parameter):
        Response(self.response).respond_parameters_missing(parameter=parameter)

    def get_jinja2(self):
        j2 = jinja2.get_jinja2(app=self.app)
        return j2

    def render_template(self, html_template, **data):
        rv = self.get_jinja2().render_template(html_template, **data)
        self.response.out.write(rv)


SELLER_PHONE_NUMBER = 'seller_phone_number'
SELLER_NAME = 'seller_name'
REGION_LOCATION_NAME = 'region_location_name'


class SellerSessionMixin(object):
    def log_in(self, name, phone_number, region_location_name):
        self.session[SELLER_NAME] = name
        self.session[SELLER_PHONE_NUMBER] = phone_number
        self.session[REGION_LOCATION_NAME] = region_location_name

    def is_seller_logged_in(self):
        return bool(self.session.get(SELLER_PHONE_NUMBER) and self.session.get(REGION_LOCATION_NAME))

    def get_seller_name(self):
        return self.session.get(SELLER_NAME)

    def get_region_location_name(self):
        return self.session.get(REGION_LOCATION_NAME)

    def get_phone_number(self):
        return self.session.get(SELLER_PHONE_NUMBER)

    def log_out(self):
        if SELLER_PHONE_NUMBER in self.session:
            self.session.pop(SELLER_PHONE_NUMBER)
        if REGION_LOCATION_NAME in self.session:
            self.session.pop(REGION_LOCATION_NAME)
