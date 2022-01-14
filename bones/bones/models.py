from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField
import datetime


class SounderModel(Document):
    service = StringField(required=True, unique=True)
    last_checked = DateTimeField(default=datetime.datetime.utcnow)
    day_interval = IntField(default=0)
    hour_interval = IntField(required=True)
    last_id = StringField()

class SpottedModel(Document):
    url = StringField()
    parsed_url = StringField()
    ipv4_address = StringField()
    ipv6_address = StringField()
    domain = StringField()
    source = StringField()
    received = DateTimeField(default=datetime.datetime.utcnow)
    country = StringField()
    registrar = StringField()
    tweet_extracted_urls = ListField(StringField())
    tweet_urls = ListField(StringField())
    tweet_hash_tags = ListField(StringField())
    tweet_text = StringField()
    tweet_id = StringField()

class GutsModel(Document):
    name = StringField(required=True)
    retrieved = DateTimeField(default=datetime.datetime.utcnow)
    storage_location = StringField(required=True)
    md5 = StringField(required=True, unique=True, max_length=32)
    sha1 = StringField(required=True, unique=True, max_length=40)
    sha256 = StringField(required=True, unique=True, max_length=64)
    ssdeep = StringField()
    original_url = ReferenceField(SpottedModel, required=True)
    associated_url = ListField(ReferenceField(SpottedModel))
