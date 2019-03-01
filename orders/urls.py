from django.conf.urls import url

from .views import OrderDeatiltview, OrderListview

urlpatterns = [
    url(r'^$', OrderListview.as_view(), name='list'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDeatiltview.as_view(), name='detail')



]