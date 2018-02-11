import webapp2

from src.handlers import PrePopulateRegionsRequest, SignUpRequest, LoginRequest, SubmitRecordRequest, \
    ListRecordsRequest, SingleRecordRequest, RegionsRequest, LogoutRequest, \
    CommonNamesRequest, IsLoggedInRequest, AverageFishPriceRequest, SmsNotificationSettingRequest
from utils.handlers import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):

        self.render_template('index.html')


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    webapp2.Route('/api/prepoluate/regions', PrePopulateRegionsRequest),

    # Seller
    webapp2.Route('/api/seller/sign_up', SignUpRequest),
    webapp2.Route('/api/seller/login', LoginRequest),
    webapp2.Route('/api/seller/is_logged_in', IsLoggedInRequest),
    webapp2.Route('/api/seller/logout', LogoutRequest),

    # Record
    webapp2.Route('/api/record/submit', SubmitRecordRequest),
    webapp2.Route('/api/records', ListRecordsRequest),
    webapp2.Route('/api/record', SingleRecordRequest),

    # Market overview
    webapp2.Route('/api/data/average_price', AverageFishPriceRequest),

    # Notification
    webapp2.Route('/api/notification/sms', SmsNotificationSettingRequest),

    # General Info
    webapp2.Route('/api/regions', RegionsRequest),
    webapp2.Route('/api/fish_names', CommonNamesRequest),

    webapp2.Route('/api/data/average_price', AverageFishPriceRequest),

    ('.*', IndexHandler),
], config=config, debug=True)


