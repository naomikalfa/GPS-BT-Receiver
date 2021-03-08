from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class BtScan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    bt_mac_addr = models.TextField(blank=False, null=False, unique=True)

    def __str__(self):
        return f'BtScan({self.bt_mac_addr})'


@receiver(pre_save, sender=BtScan)
def pre_save_btscan(sender, instance=None, created=False, **kwargs):
    if instance is not None and instance.bt_mac_addr is not None:
        instance.bt_mac_addr = instance.bt_mac_addr.upper()
        instance.bt_mac_addr.replace('\n', '')
        instance.bt_mac_addr.replace('\r', '')


#  create BtService ORM object and little_maze all of the find.services properties to this object
# need a foreign key to the BtScan model to be able to link correctly
class BtService(models.Model):
    btscan = models.ForeignKey(BtScan, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    service_classes = models.TextField(blank=True, null=True)
    profiles = models.TextField(blank=True, null=True)
    provider = models.TextField(blank=True, null=True)
    service_id = models.TextField(blank=True, null=True)
    protocol = models.TextField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    host = models.TextField(blank=True, null=True)




















