from bluetooth.ble import DiscoveryService  # noqa
from bt_scan.models import BtScan
from django.core.management.base import BaseCommand
from gps_scan.tasks import bt_device_service_discovery

from datetime import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        while True:

            service = DiscoveryService()
            devices = service.discover(20)

            for address in devices:
                address = str(address)
                address = address.strip()

                try:
                    b = BtScan.objects.get(bt_mac_addr=address.upper())
                    b.last_seen = datetime.now()
                    b.save()
                    print('Already known', address)

                except BtScan.DoesNotExist:
                    #  if new device, store it in this table then send off to workers to query it for services
                    b = BtScan()
                    b.created_at = datetime.now()
                    b.last_seen = datetime.now()
                    b.bt_mac_addr = address
                    b.save()
                    print('New device', address)

                    bt_device_service_discovery.delay(address)


