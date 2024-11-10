from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(UserContact)
admin.site.register(UserContactMapping)
admin.site.register(UserProfile)