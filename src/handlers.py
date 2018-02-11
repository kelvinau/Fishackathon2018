import base64
import urllib
from datetime import date, datetime, timedelta

import logging

import requests

import urlfetch

from src.models import Seller, Region, Record, Fish
from utils.general import get_param
from utils.handlers import BaseHandler, SellerSessionMixin

from google.appengine.ext import ndb

from utils.twilio_helper import send_sms


class SignUpRequest(BaseHandler, SellerSessionMixin):
    def post(self):

        name = get_param(self.request, 'name')
        location = get_param(self.request, 'location')
        phone_number = get_param(self.request, 'phone_number')
        password = get_param(self.request, 'password')

        seller = Seller(id=Seller.generate_id_by_phone_number(phone_number), name=name, location=location,
                        phone_number=phone_number, password=password)
        seller.put()

        self.log_in(name, phone_number, location)

        self.response_success("Success", data={'user': seller.to_dict()})


class LoginRequest(BaseHandler, SellerSessionMixin):
    def post(self):

        phone_number = get_param(self.request, 'phone_number')
        password = get_param(self.request, 'password')

        seller_id = Seller.generate_id_by_phone_number(phone_number)
        seller_key = Seller.build_key_by_id(seller_id)

        seller = seller_key.get()

        if seller:
            if seller.password == password:

                self.log_in(seller.name, seller.phone_number, seller.location)

                self.response_success("Success", data={'user':seller.to_dict()})
            else:
                self.response_failure("Password incorrect")
        else:
            self.response_permission_denied("Phone number doesn't exist")


class LogoutRequest(BaseHandler, SellerSessionMixin):
    def post(self):
        if not self.is_seller_logged_in():
            self.response_permission_denied('User not logged in')
            return

        self.log_out()
        self.response_success('User is successfully logged out')


class SubmitRecordRequest(BaseHandler, SellerSessionMixin):
    def post(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        location_name = self.get_region_location_name()
        region_id = Region.generate_id_by_location_name(location_name)
        region_key = Region.build_key_by_id(region_id)
        region = region_key.get()

        phone_number = self.get_phone_number()
        seller_id = Seller.generate_id_by_phone_number(phone_number)
        seller_key = Seller.build_key_by_id(seller_id)
        seller = seller_key.get()

        price = int(get_param(self.request, 'price'))
        fish_common_name = get_param(self.request, 'fish_name')
        caught_date = get_param(self.request, 'caught_date')
        caught_date = datetime.strptime(caught_date, '%Y-%m-%d')

        submitted_date = date.today()

        fish = self.get_fish_by_common_name(region, fish_common_name)

        record = Record(id=Record.generate_id(), seller=seller, region=region, fish=fish, caught_date=caught_date,
                        submitted_date=submitted_date, price=price)
        record.put()
        self.response_success("Success")

    def get_fish_by_common_name(self, region, common_name):
        for fish in region.fish_names:
            if common_name == fish.common_name:
                return fish


class ListRecordsRequest(BaseHandler, SellerSessionMixin):
    def get(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        fish_name = get_param(self.request, 'fish_name')

        location_name = self.get_region_location_name()

        if fish_name:
            q = Record.query(ndb.AND(Record.region.location_name == location_name,
                                     Record.fish.common_name == fish_name))
        else:
            q = Record.query(Record.region.location_name == location_name)

        qs = q.fetch()
        records = [record.to_dict() for record in qs]

        self.response_success("Success", data=records)


class SingleRecordRequest(BaseHandler, SellerSessionMixin):
    def get(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        id = get_param(self.request, 'id')
        record_key = Record.build_key_by_id(id)
        record = record_key.get()
        self.response_success("Success", data=record.to_dict())


class PrePopulateRegionsRequest(BaseHandler):
    def get(self):

        fixed_region_values= {
            'Vancouver': {
                'fish_names': [
                    {
                        'common_name': 'Blue Cod',
                        'scientific_name': 'Parapercis Colias'
                    },
                    {
                        'common_name': 'Chinook Salmon',
                        'scientific_name': 'Oncorhynchus Tshawytscha'
                    }
                ],
                'lat': 49.2827,
                'lng': -123.1207
            },
            'Victoria': {
                'fish_names': [
                    {
                        'common_name': 'King Salmon',
                        'scientific_name': 'Oncorhynchus Tshawytscha'
                    },
                    {
                        'common_name': 'North Pacific Bluefin Tuna',
                        'scientific_name': 'Thunnus Orientalis'
                    }
                ],
                'lat': 48.4284,
                'lng': -123.3656
            },
            'Toronto': {
                'fish_names': [
                    {
                        'common_name': 'Northern Bluefin Tuna',
                        'scientific_name': 'Thunnus Orientalis'
                    },
                    {
                        'common_name': 'MoonFish',
                        'scientific_name': 'Mene Maculata'
                    }
                ],
                'lat': 43.6532,
                'lng': -79.3832
            },
        }

        for name in fixed_region_values:

            region_values = fixed_region_values[name]
            fish = [Fish(common_name=fish_value['common_name'], scientific_name=fish_value['scientific_name']) for
                    fish_value in region_values['fish_names']]

            region_id = Region.generate_id_by_location_name(name)
            region = Region(id=region_id, location_name=name, fish_names=fish, lat=region_values['lat'],
                            lng=region_values['lng'])
            region.put()

        self.response_success("Done")


class RegionsRequest(BaseHandler, SellerSessionMixin):
    def get(self):
        regions = Region.query().fetch()
        regions = [region.to_dict() for region in regions]
        self.response_success("List of regions", data=regions)


class CommonNamesRequest(BaseHandler, SellerSessionMixin):
    def get(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        location_name = self.get_region_location_name()

        region_id = Region.generate_id_by_location_name(location_name)
        region_key = Region.build_key_by_id(region_id)

        region = region_key.get()
        fish_names = [fish_name.to_dict() for fish_name in region.fish_names]

        self.response_success("List of fish names for your region", data=fish_names)


class IsLoggedInRequest(BaseHandler, SellerSessionMixin):
    def get(self):
        region_lat, region_lng, seller = None, None, None
        if self.is_seller_logged_in():
            region_id = Region.generate_id_by_location_name(self.get_region_location_name())
            region_key = Region.build_key_by_id(region_id)
            region = region_key.get()
            region_lat = region.lat
            region_lng = region.lng

            seller_phone_number = self.get_phone_number()
            seller_id = Seller.generate_id_by_phone_number(seller_phone_number)
            seller_key = Seller.build_key_by_id(seller_id)
            seller = seller_key.get()

        self.response_success("Log in status is successfully retrieved",
                              data={'logged_in': self.is_seller_logged_in(), 'user': seller.to_dict() if seller else None,
                                    'lat': region_lat,
                                    'lng': region_lng})


class AverageFishPriceRequest(BaseHandler, SellerSessionMixin):
    def get(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        common_name = get_param(self.request, 'fish_name')
        location_name = self.get_region_location_name()

        scientific_name = self.fetch_scientific_name(location_name, common_name)

        last_month = date.today() - timedelta(days=30)

        qs = Record.query(ndb.AND(Record.fish.scientific_name == scientific_name, Record.submitted_date >= last_month))
        qs = qs.fetch()

        region_lat_lng = {}
        region_price_list = {}
        for record in qs:
            if region_price_list.get(record.region.location_name):
                region_price_list[record.region.location_name].append(record.price)
            else:
                region_lat_lng[record.region.location_name] = {'lat': record.region.lat, 'lng': record.region.lng}
                region_price_list[record.region.location_name] = [record.price]

        region_avg_price = {}
        for avg_mapping in region_price_list:
            region_avg_price[avg_mapping] = \
                {'average': sum(region_price_list[avg_mapping]) / float(len(region_price_list[avg_mapping])),
                 'lat': region_lat_lng[avg_mapping]['lat'],
                 'lng': region_lat_lng[avg_mapping]['lng']
                 }

        self.response_success("Success", data=region_avg_price)

    def fetch_scientific_name(self, location_name, common_name):
        region_id = Region.generate_id_by_location_name(location_name)
        region_key = Region.build_key_by_id(region_id)
        region = region_key.get()

        for fish_name in region.fish_names:
            if fish_name.common_name == common_name:
                return fish_name.scientific_name


class SmsNotificationSettingRequest(BaseHandler, SellerSessionMixin):
    def post(self):

        if not self.is_seller_logged_in():
            self.response_permission_denied('User is not logged in')
            return

        seller_phone = self.get_phone_number()
        seller_id = Seller.generate_id_by_phone_number(seller_phone)
        seller_key = Seller.build_key_by_id(seller_id)

        set_sms_notification = bool(get_param(self.request, 'notification_on'))

        seller = seller_key.get()
        seller.sms_notification = set_sms_notification
        seller.put()

        # todo comment out
        if set_sms_notification:
            logging.info('Sending sms to %s', seller.phone_number)
            sms_sent = send_sms(seller.phone_number, 'Thank you for your interest. You will receive news from us.')
            if sms_sent:
                logging.info('SMS was sent successfully')
            else:
                logging.info('Failed to send SMS')

        self.response_success("SMS notification setting is successful")
