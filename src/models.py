import uuid

from google.appengine.ext import ndb
import hashlib


class Seller(ndb.Model):
    location = ndb.StringProperty()
    name = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    password = ndb.StringProperty()
    sms_notification = ndb.BooleanProperty(default=False)

    @classmethod
    def build_key_by_id(cls, id):
        return ndb.Key(cls, id)

    @classmethod
    def generate_id_by_phone_number(cls, phone_number):
        id = hashlib.md5()
        id.update(phone_number)
        return id.hexdigest()


class Fish(ndb.Model):
    scientific_name = ndb.StringProperty()
    common_name = ndb.StringProperty()


class Region(ndb.Model):
    location_name = ndb.StringProperty()
    fish_names = ndb.StructuredProperty(Fish, repeated=True)
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()

    @classmethod
    def build_key_by_id(cls, id):
        return ndb.Key(cls, id)

    @classmethod
    def generate_id_by_location_name(cls, location_name):
        id = hashlib.md5()
        id.update(location_name)
        return id.hexdigest()


class Record(ndb.Model):
    seller = ndb.StructuredProperty(Seller)
    region = ndb.StructuredProperty(Region)
    fish = ndb.StructuredProperty(Fish)
    caught_date = ndb.DateProperty()
    submitted_date = ndb.DateProperty()

    # Cents the fish sold for
    price = ndb.IntegerProperty()

    @classmethod
    def build_key_by_id(cls, id):
        return ndb.Key(cls, id)

    @classmethod
    def generate_id(cls):
        id = uuid.uuid4()
        return str(id)

    def to_dict(self):
        value = super(Record, self).to_dict()
        value['id'] = self.key.id()
        value['caught_date'] = self.caught_date.strftime('%Y-%m-%d')
        value['submitted_date'] = self.submitted_date.strftime('%Y-%m-%d')
        return value
