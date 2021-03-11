from datetime import *
from django.core.management.base import BaseCommand
from gps_scan.tasks import deep_scan_gps_location
from gps_scan.models import GpsScan
import gpsd
import random
from time import time, sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        gpsd.connect() 
        packet = gpsd.get_current()

        last_lat = None
        last_lon = None

        while True:
            
            current_position = packet.position()  # position = lat x lon
            print(current_position)
            if last_lat is not None and last_lon is not None:

                    current_lat = current_position[0]
                    current_lon = current_position[1]

                    if random.randrange(0, 100) > 80:
                        current_lat += 10
                        current_lon += 8

                    diff_lat = abs(current_lat - last_lat)
                    diff_lon = abs(current_lon - last_lon)
                    print(diff_lat, diff_lon)

                    if diff_lat >= 5:
                        if diff_lon >= 5:

                            g = GpsScan()
                            g.created_at = datetime.now()
                            g.lat = current_position[0]
                            g.lon = current_position[1]
                            g.save()

                            last_lat = current_position[0]
                            last_lon = current_position[1]

    deep_scan_gps_location.delay()
