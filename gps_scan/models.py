from django.db import models


class GpsScan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(blank=False, null=False)
    lon = models.FloatField(blank=False, null=False)
    other = models.TextField(blank=True, null=True)
