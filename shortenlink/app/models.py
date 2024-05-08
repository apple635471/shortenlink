from django.db import models


# Create your models here.
class URLMapping(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class URLTracking(models.Model):
    id = models.AutoField(primary_key=True)
    url_mapping = models.ForeignKey(URLMapping, on_delete=models.CASCADE)
    # owner = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)
