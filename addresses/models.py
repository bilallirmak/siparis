from django.db import models
from django.db.models import Count, Avg, Sum
from billing.models import BiliingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class AddressManagerQuerySet(models.query.QuerySet):
    def by_state(self, state=None):
        return self.aggregate(Count(state))

class Address(models.Model):
    billing_profile = models.ForeignKey(BiliingProfile, verbose_name="Faturalama profili")
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES, verbose_name="Adres Tipi")
    address_line_1 = models.CharField(max_length=200, verbose_name="Adres 1")
    address_line_2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Adres 2")
    city = models.CharField(max_length=120, default="Izmir", verbose_name="Şehir")
    country = models.CharField(max_length=120, default="Turkiye", verbose_name="Ülke")
    state = models.CharField(max_length=120, verbose_name="İlçe")
    # postal_code = models.CharField(max_length=120)

    def __str__(self):
        return "{line1}\n{line2}\n{city}\n{state}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            state=self.state
        )
        # return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            state=self.state
        )



