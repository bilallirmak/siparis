from django.conf.urls import url
from django.views.generic import RedirectView
from .views import *
from products.views import UserProductHistoryView
app_name = "account"

urlpatterns = [

    url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^login/$', RedirectView.as_view(url='browse')),
    # url(r'^login/$', login_view, name='login'),
    url(r'^register/guest/$', guest_register_view, name='guestregister'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^$', AccountHomeView.as_view(), name='accounthome'),
    url(r'^history/products/$', UserProductHistoryView.as_view(), name='user-product-history'),

]