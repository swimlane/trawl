from mongoengine import connect
from .models import SounderModel
from .entrail import Entrail



class Sounder(Entrail):
     
    def save(self, service, last_checked=None, day_interval=0, hour_interval=None, last_id=None):
        sounder = SounderModel(
            service=service,
            last_checked=None,
            day_interval=day_interval,
            hour_interval=hour_interval,
            last_id=last_id
        ).save()

    def get(self, service=None):
        if service:
            try:
                return SounderModel.objects.get(service=service)
            except:
                return None
        else:
            return SounderModel.objects
            
            