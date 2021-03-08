from django.contrib import admin
from bt_scan.models import BtScan, BtService


class BtScanAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'last_seen', 'bt_mac_addr')


class BtServiceAdmin(admin.ModelAdmin):
    list_display = ('btscan', 'description', 'name', 'service_classes', 'profiles', 'provider', 'service_id',
                                                                                                'protocol', 'port', 'host')

admin.site.register(BtScan, BtScanAdmin)

admin.site.register(BtService, BtServiceAdmin)
