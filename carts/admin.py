from django.contrib import admin
from .models import Cart, CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product' ]
    # list_editable = ['active', 'price','category']

    class Meta:
        model = CartItem
class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', '__unicode__']
    # list_editable = ['active', 'price','category']

    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

