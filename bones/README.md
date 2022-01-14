# Bones

Bones is a Python package to save and retrieve information from a mongodb database.

This package is used by both `spotter` and `trawler` to retrieve, save, and communicate with `entrails` (MongoDB container)

## Models

The mongodb (chum) docker container has the following defined models for different document types.  Please view the following for more information about these models:


### Sounder Model

Sounder is used to store service configuration based on your `config.yml`.  Each service has it's own document and is used to drive the schedule of when each service is checked.

```python
service = StringField(required=True, unique=True)
last_checked = DateTimeField(default=datetime.datetime.utcnow)
day_interval = IntField(default=0)
hour_interval = IntField(required=True)
last_id = StringField()
```

### Spotted Model

Any new URLs identified and are added to the RabbitMQ queue to be trawled are first added to the Spotted document.  This is so that we do not continually check a previously known URL but also to relate the source of the identified URL with the findings - which are store in the Guts Model and associated via a reference field in the Guts document.

```python
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
```

### Guts Model

The Guts model is used to store downloaded kits and other files downloaded when a URL is trawled.

```python
name = StringField(required=True)
retrieved = DateTimeField(default=datetime.datetime.utcnow)
storage_location = StringField(required=True)
md5 = StringField(required=True, unique=True, max_length=32)
sha1 = StringField(required=True, unique=True, max_length=40)
sha256 = StringField(required=True, unique=True, max_length=64)
ssdeep = StringField()
original_url = ReferenceField(SpottedModel, required=True)
associated_url = ListField(ReferenceField(SpottedModel))
```