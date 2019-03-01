from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.urls import reverse
from products.models import Product


User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True) #sonradan eklendi
    # user = models.ForeignKey(User, null=True, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    line_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2) # sonradan ekelndi
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.product.slug})

    def __str__(self):

        try:
            return str(self.cart.id)
        except:
            return self.product.title

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

    @property
    def name(self):
        return self.product.title

class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True, related_name="items")
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug":self.products.slug})

    def __str__(self):
        liste = ""
        for i in self.items.all():
            liste = liste + str(i.product.title) + ',' # + '('+str(i.quantity)+')'
        return liste

    def __unicode__(self):
        return self.id

    @property
    def name(self):
        return self.products.title


# def m2m_changed_q_receiver(sender, instance, action, *args, **kwargs):
#
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.items.all()
#         total = 0
#         line_total = 0
#         for x in products:
#             line_total += (x.product.price)*(x.quantity)
#             x.line_total = line_total
#             total += x.line_total
#             instance.subtotal = x.line_total
#             instance.save()
#             x.save()
#             # instance.objects.filter(cart_id=cart_obj.id).update(line_total=Decimal(x.line_total))
#
#             total = 0
#             line_total = 0
#         # instance.save()
#
#         # products = instance.products.all()
#         # total = 0
#         # line_total = 0
#         # for x in products:
#         #     total += x.price
#         #     if instance.subtotal != total:
#         #         instance.subtotal = total
#         #         instance.save()
#
# m2m_changed.connect(m2m_changed_q_receiver, sender=Cart.items.through)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        # products = instance.products.all()
        quantitys = instance.items.all()

        total = 0
        query=0
        liste_example = [[],[],[],[],[]]
        toplam=0


                        # instance.objects.filter(cart_id=cart_obj.id).update(line_total=Decimal(x.line_total))

        for y in quantitys:
            liste_example[0].append(y.product.id)
            liste_example[1].append(y.quantity)
            liste_example[2].append(y.product.price)
            # liste_example[3].append(y.quantity * y.product.price)
        print(liste_example)


        for x in quantitys:


            z=liste_example[2][query]*liste_example[1][query]
            print(z)
            # if z / liste_example[2][query] == liste_example[1][query] and liste_example[0][query] == x.product.id:
            if liste_example[0][query] == x.product.id:
                liste_example[3].append(z)
                total = total + z
                toplam = total + toplam

                print ("TOTALİM BENİM",total)
                line_total = z
                x.line_total = line_total

                Cart.objects.filter(id=y.cart.id).update(total=Decimal(total))
                x.save()
                query += 1

            else:
                query += 1

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    # instance.total = Decimal(instance.subtotal) * Decimal(1.18)
    instance.total = instance.subtotal
pre_save.connect(pre_save_cart_receiver, sender=Cart)