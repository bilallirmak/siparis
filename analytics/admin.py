from django.contrib import admin

from .models import ObjectViewed, UserSession

class ObjectAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'timestamp', 'ip_address']

    class Meta:
        model = ObjectViewed

admin.site.register(ObjectViewed, ObjectAdmin)
admin.site.register(UserSession)

