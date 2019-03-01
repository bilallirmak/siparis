from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BiliingProfile
from products.models import Product
from orders.models import Order
from .models import Cart, CartItem
from decimal import *
import sqlite3
from django.db.models import F

def cart_q_add_view(request):
    product_id = request.POST.get('product_id')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if not product_obj in cart_obj.items.all():

            print('IDDDDDDDDDDDDDD',cart_item.cart_id)
            print('IDD',cart_obj.id)
            # CartItem.objects.all().update(quantity=F('quantity') + 1)
            print("slmmmmmmmmmmm")
            f = cart_item.product.price
            e = cart_obj.total
            a = cart_item.quantity + 1
            CartItem.objects.filter(cart_id=cart_obj.id).filter(product_id=product_obj).update(quantity=a)
            c = cart_item.product.price * a
            print(c)
            CartItem.objects.filter(cart_id=cart_obj.id).filter(product_id=product_obj).update(line_total=c)
            Cart.objects.filter(id=cart_item.cart_id).filter(products=product_obj).update(total=f+e)

        else:
            print("assssssssssssssss")

    # return render(request, 'carts/snippets/cart_q_add.html', {'cart': cart_obj})
    # Cart.objects.filter(id=y.cart.id).update(total=Decimal(total))

    return redirect('cart:homecart')
def cart_q_remove_view(request):
    product_id = request.POST.get('product_id')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if not product_obj in cart_obj.items.all():
            f = cart_item.product.price
            e = cart_obj.total
            b=cart_item.quantity - 1

            if b<1:
                return redirect('cart:homecart')
            else:
                CartItem.objects.filter(cart_id=cart_obj.id).filter(product_id=product_obj).update(quantity=b)
                d = cart_item.product.price * b
                print(b)
                CartItem.objects.filter(cart_id=cart_obj.id).filter(product_id=product_obj).update(line_total=d)
                Cart.objects.filter(id=cart_item.cart_id).filter(products=product_obj).update(total=e-f)
        else:
            print("assssssssssssssss")

    # return render(request, 'carts/snippets/cart_q_add.html', {'cart': cart_obj})
    # Cart.objects.filter(id=y.cart.id).update(total=Decimal(total))

    return redirect('cart:homecart')



def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    da=0
    paraListe=[]
    # dd = 0
    # products = [{"id": x.id, "url": x.get_absolute_url(), "name": x.name, "price": x.price} for x in cart_obj.products.all()]
    products = [{"id": i.product.id, "url": i.get_absolute_url(), "name": i.name, "quantity": i.quantity, "line_total": i.line_total, "price": i.product.price, "total": cart_obj.total} for i in cart_obj.items.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    global toplam
    global t
    toplam = 0
    urunSay = len(products)
    # products = [{"quantity": i.quantity, "line_total": i.line_total} for i in cart_obj.items.all()]


#NOT: products[da]["line_total"] KISMINA PRODUCT'DAN PRİCE DEĞERİ ÇEKİLMEK ZORUNDA!
#YADA HERBİR CART İTEMIN KENDİNE AİT SABİT PRİCE DEĞERİ OLMALI!
    for a in products:
        ka=a["id"]
        z=a["quantity"]*a["line_total"]
        b={"line_total": z}
        if z/products[da]["price"]==products[da]["quantity"] and ka == products[da]["id"]:
            products[da].update(b)
            toplam = toplam + z
            # CartItem.objects.filter(cart_id=cart_obj.id).update(line_total=Decimal(z))
            # Cart.objects.filter(id=cart_obj.id).update(total=Decimal(toplam))
            # cart_obj.filter(cart_obj=kc).update(line_total=Decimal(z))
            # t = CartItem.objects.get(cart=cart_obj.id)
            # t.line_total = Decimal(z)
            print (cart_obj.id)
            # t.save()
            da += 1
        else:
            da += 1

    # t = Cart.objects.get(id=cart_obj.id)
    # cart_obj.filter(cart_obj).update(line_total=Decimal(z))

    for g in cart_data:
        ca=cart_data["subtotal"]
        ce={"subtotal": Decimal(toplam)}
        snake = {"total": products[0]["total"]}

        if ca!=toplam:
            cart_data.update(ce)
            cart_data.update(snake)
        else:
            cart_data.update(ce)
            cart_data.update(snake)
            return JsonResponse(cart_data)





    # for a in products:
    #     z=a["quantity"]*a["line_total"]
    #     b={"line_total": z}
    #     if z/products[da]["line_total"]==products[da]["quantity"]:
    #         products[da].update(b)
    #         da += 1
    #     else:
    #         da += 1
        # i['line_total']=(i['quantity']*i['line_total'])
        # print(i['line_total'])
    # metin =""
    # for a in quantity:
    #     products[da].update(a)
    # print(a)
    # for w in products:
    #     metin = metin+w
    # products = products+quantity
    # products = list(products)
    # print(products[0])
    # products[0].update(products[2])
    # print(products[0])
    # products = dict(zip(products, quantity))


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/homecart.html", {'cart': cart_obj})




def cart_update(request):

    product_id = request.POST.get('product_id')

    if product_id is not None:

        try:
            product_obj = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return redirect("cart:homecart")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        # t = Cart.objects.get(id=cart_obj.id)
        # t.total = Decimal(toplam)
        # t.save()
        # print("t-total:", t.total)
        if created:
            print("Olumlu")



        # if cart_item.cart == None:
        #
        # else:
        #     pass


        # if not cart_item in cart_obj.items.all():
        #     # added = False
        #     # cart_obj.items.add(cart_item)   #sonradan yourum satırı yapıldı
        #     cart_obj.items.add(cart_item)
        # else:
        #     # added = True
        #     cart_obj.items.remove(cart_item)
        if not cart_item in cart_obj.items.all():
                    # added = False

            cart_obj.items.add(cart_item)
        else:
            # added = True
            # cart_obj.items.remove(cart_item)
            cart_item.delete()

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True



        # for item in cart_obj.items.all():
        #     line_total += item.product.price * item.quantity
        #     item.line_total = line_total
        #     item.save()
        #     cart_obj.total = item.line_total
        #     line_total = 0

        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added":added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }

            return JsonResponse(json_data, status=200)
            # return JsonResponse({"message": "Error 400"}, status=400)
    return redirect("cart:homecart")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:homecart")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BiliingProfile.objects.new_or_get(request)

    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")



    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }

    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})

def adres_ekle(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:homecart")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BiliingProfile.objects.new_or_get(request)

    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }


    return render(request, "addresses/add_address.html", context)