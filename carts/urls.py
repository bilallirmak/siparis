from django.conf.urls import url

from .views import(
    cart_home,
    cart_update,
    checkout_home,
    checkout_done_view,
    adres_ekle,
    cart_q_add_view,
    cart_q_remove_view
    )

urlpatterns = [

    url(r'^$',cart_home, name='homecart'),
    url(r'^checkout/$', checkout_home, name='checkoutcart'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    url(r'^update/$', cart_update, name='updatecart'),
    url(r'^adres-ekle/$', adres_ekle, name='adrescart'),
    url(r'^add-q/$', cart_q_add_view, name='addq'),
    url(r'^remove-q/$', cart_q_remove_view, name='removeq'),

]
