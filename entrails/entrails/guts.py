from mongoengine import connect
import datetime
from .models import GutsModel
from .models import SpottedModel
from .entrail import Entrail


class Guts(Entrail):
     
    def save(self, name, storage_location, md5, sha1, sha256, original_url, timestamp=None, ssdeep=None):
        spotted = SpottedModel().objects(url=original_url)

        # If no spotted document then create one and retrieve it from our db
        if not spotted:
            self.spotted = SpottedModel(original_url)
            spotted = SpottedModel().objects(url=original_url)
            
        guts = GutsModel(
            name=name,
            storage_location=storage_location,
            md5=md5,
            sha1=sha1,
            sha256=sha256,
            ssdeep=ssdeep,
            original_url=spotted,
            timestamp=datetime.datetime.utcnow() if timestamp is None else timestamp
        ).save()