"""siparis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import (url, include)
from django.contrib import admin
from home.views import (home_view, about_page, contact_page)
from analytics.views import SalesView, SalesAjaxView
from addresses.views import (checkout_address_create_view, checkout_address_reuse_view)
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from carts.views import cart_detail_api_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home_view, name='home'),
    url(r'^browse/$',home_view, name='browse'),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    url(r'^about/$',about_page,name='about'),
    url(r'^contact/$',contact_page,name='contact'),
    url(r'^analytics/sales/$',SalesView.as_view(), name='sales-analytics'),
    url(r'^analytics/sales/data/$', SalesAjaxView.as_view(), name='sales-analytics-data'),
    url(r'^accounts/', RedirectView.as_view(url='/account/login')),
    url(r'^account/', include('accounts.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^settings/', RedirectView.as_view(url='/account')),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    url(r'^api/cart/$', cart_detail_api_view, name="api-cart"),
    url(r'^cart/', include('carts.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
