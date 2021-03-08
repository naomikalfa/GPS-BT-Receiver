# Create your tasks here
import bluetooth
from bt_scan.models import BtScan, BtService
from celery import shared_task
import logging


@shared_task()
def bt_device_service_discovery(address):
    logging.info(f'BTService on address {address} starting.')
    #  celery worker execution starts

    services = bluetooth.find_service(address=address)

    # load btScan ORM model with address btScan.objects.get() - this is row with hardware ID
    device = BtScan.objects.get(bt_mac_addr=address)  # instantiates the device to be worked upon below

    if len(services) <= 0:
        print("zero services found on", device)

    else:
        for service in services:
            b = BtService()
            b.btscan = device  # this feeds the device address into each service request
            b.description = service['description']
            print(service['description'])
            b.name = service['name']
            print(service['name'])
            b.service_classes = service['service-classes']
            print(service['service-classes'])
            b.profiles = service['profiles']
            print(service['profiles'])
            b.provider = service['provider']
            print(service['provider'])
            b.service_id = service['service-id']
            print(service['service-id'])
            b.protocol = service['protocol']
            print(service['protocol'])
            b.port = service['port']
            print(service['port'])
            b.host = service['host']
            print(service['host'])
            b.save()
#  Create bt_Service ORM object and map all of the service properties to this object and .save()
#  one of the worker's first jobs will be to pull row from db using method of object.get()


@shared_task()
def deep_scan_gps_location():
    pass

