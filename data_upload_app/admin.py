from django.contrib import admin

# Register your models here.

from .models import UserFileInfo, UserModelDetails

admin.site.register(UserFileInfo)
admin.site.register(UserModelDetails)
