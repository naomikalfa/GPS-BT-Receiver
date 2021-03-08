from django.contrib import admin
from gps_scan.models import GpsScan


class GpsScanAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'lat', 'lon', 'other')


admin.site.register(GpsScan, GpsScanAdmin)

