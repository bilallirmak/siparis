import math
import datetime
from django.utils import timezone
from django.db import models
from django.db.models import Count, Avg, Sum
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from billing.models import BiliingProfile
from carts.models import Cart
from addresses.models import Address
from siparis.utils import unique_order_id_generator
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def by_billing_profile(self, request):
        billing_profile, created = BiliingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def recent(self):
        return self.order_by("-updated", "-timestamp")

    def get_sales_breakdown(self):

        recent = self.recent().not_refunded().not_created()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data

        }
        return data

    def by_weeks_range(self, weeks_ago=1, number_of_weeks=1):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date=end_date).not_created()

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

    def by_date(self):
        now = timezone.now() #- datetime.timedelta(days=7)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def cart_data(self):
        return self.aggregate(Sum("cart__products__price"),
                              Avg("cart__products__price"),
                              Count("cart__products"),
                              )

    def by_status(self, status="shipped"):
        return self.filter(status=status)
    def not_refunded(self):
        return self.exclude(status="refunded")
    def not_created(self):
        return self.exclude(status="created")

    def by_request(self, request):
        billing_profile, created = BiliingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')



class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    # def by_billing_profile(self, request):
    #     return self.get_queryset().by_billing_profile(r)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True

        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BiliingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True,verbose_name="Sip. NO")
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, verbose_name="Adres")
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True)
    cart = models.ForeignKey(Cart, verbose_name="Sepet")
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES, verbose_name="Durum")
    shipping_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name="Toplam(TL)")
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Tarih")

    def __str__(self):
        return self.order_id

    def __unicode__(self):
        p_liste = ""
        for i in self.cart.items.all():
            p_liste = p_liste + str(i.product.title) + '(' +str(i.quantity)+')' + ','
        return p_liste


    objects = OrderManager()

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id':self.order_id})

    def get_status(self):
        if self.status == 'refunded':
            return "İade"
        elif self.status == 'shipped':
            return "Teslim Edildi"
        return "Sipariş Yolda"
    class Meta:
        ordering = ['-timestamp', '-updated']

    # def get_absolute_url(self):
    #     return reverse("orders:detail", kwargs={'order_id':self.order_id})


    # def q_list(self):
    #     liste = []
    #     for i in self.cart.items.all():
    #         liste.append(i.quantity * str(i.product.title) + ',')
    #
    #     return liste

    # def get_status(self):
    #     if self.status == "refunded":
    #         return "Ürün iadesi"
    #     elif self.status == "shipped":
    #         return "Teslim Edildi"
    #
    #     return "Şu an Yolda"

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formated_total = format(new_total, ".2f")
        self.total = formated_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False
    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)
