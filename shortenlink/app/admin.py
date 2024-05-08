from django.contrib import admin

from .models import URLMapping, URLTracking

# Register your models here.
admin.site.register(URLMapping)
admin.site.register(URLTracking)
