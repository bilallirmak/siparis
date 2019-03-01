from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'shipping_address', '__unicode__', 'timestamp','status', 'total']
    ordering = ['-timestamp']

admin.site.register(Order, OrderAdmin)


