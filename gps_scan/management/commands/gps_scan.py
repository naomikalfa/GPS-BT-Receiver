from django.core.management.base import BaseCommand
import gpsd
from datetime import *
from time import time, sleep
from gps_scan.models import GpsScan
import random
from gps_scan.tasks import deep_scan_gps_location


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        gpsd.connect()  # host="127.0.0.1", port=2947
        packet = gpsd.get_current()

        last_lat = None
        last_lon = None

        while True:

            #  to filter on the date added that is older than 10 seconds old
            #  GpsScan.objects.filter(created_at__date__gte=datetime.now()-timedelta(seconds=10))
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


"""''
#  check timestamp from field created_at datetimeField
#  if timestamp is older than 600 seconds, run amd write a scan

checking_ten_minutes = datetime.now() - timedelta(seconds=600)
ten_min = str(checking_ten_minutes)
parsed_ten = ten_min[11:26]

GpsScan.created_at.filter(date__range=[datetime.now(), checking_ten_minutes])




'''


#sleep(600)

# p = GpsScan.objects.values_list('created_at').annotate()
# p = GpsScan.objects.values_list('created_at').order_by('-created_at')
# p[0] == most recent entry

#now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
"""