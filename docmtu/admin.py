from django.contrib import admin

from .models import Changelog, DiningLocation
# Register your models here.

admin.site.register(DiningLocation)
admin.site.register(Changelog)
