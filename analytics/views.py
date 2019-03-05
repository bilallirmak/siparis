import locale
import random
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Avg
from django.views.generic import TemplateView, View
from django.shortcuts import render
from orders.models import Order
from django.utils import timezone
from addresses.models import Address
from carts.models import Cart
try:
    locale.setlocale(locale.LC_ALL, "tr")
except locale.Error:
    pass
class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get('type') == 'week':
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(new_time)

                    labels.append(
                        new_time.strftime("%a")
                    )

                    new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
                    day_total = new_qs.totals_data()['total__sum'] or 0

                    salesItems.append(
                        day_total
                    )

                data['labels'] = labels
                data['data'] = salesItems
                data['ctip'] = 'line'
                data['etiket'] = 'Satışlar(TL)'

            if request.GET.get('type') == '4weeks':
                data['labels'] = ['Dört hafta önce', 'Üç hafta önce', "İki hafta önce", "Bir hafta önce",]
                data['ctip'] = 'line'
                data['etiket'] = 'Satışlar(TL)'
                current = 5

                data['data'] = []

                for i in range(1, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()['total__sum'] or 0
                    data['data'].append(sales_total)
                    current -= 1



            liste =[]
            if request.GET.get('type') == 'product':
                carts = Order.objects.all().not_created()
                for product in carts:
                    liste.append(str(product.cart))

                liste2 = []
                metin = ""

                for i in liste:
                    metin = metin + str(i)

                lite = metin.split(',')

                kume = set()
                for i in lite:
                    kume.add(i)
                kume = list(kume)
                yedek_kume = kume
                datas = []
                for j in kume:
                    datas.append(lite.count(j))
                datas_yedek = datas

                veriler = []
                etiketler = []
                for x in range(5):
                    maxFind = max(datas)
                    findIndex = datas.index(maxFind)
                    findItemValue = datas[findIndex]
                    findItem = kume[findIndex]
                    veriler.append(findItemValue)
                    etiketler.append(findItem)

                    kume.pop(findIndex)
                    datas.pop(findIndex)

                data['labels'] = etiketler
                data['data'] = veriler
                data['ctip'] = 'bar'
                data['etiket'] = 'Satışlar(Adet)'

            liste_n = []
            if request.GET.get('type') == 'product-week':
                new_carts = Order.objects.all().not_created().by_weeks_range(weeks_ago=5, number_of_weeks=5)
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days - 1)
                datetime_l = []
                etiketler1 = []
                veriler1 = []

                for x in range(0, days):
                    new_time1 = start_date + datetime.timedelta(days=x)
                    datetime_l.append(new_time1)

                    # etiketler1.append(
                    #     new_time.strftime("%a")
                    # )

                    new_q = new_carts.filter(updated_day=new_time1.day, updated_month=new_time1.month)
                    # day_t = new_q.totals_data()["cart__products"] or 0
                    # veriler1.append(day_t)
                    for product in new_q:
                        liste_n.append(str(product.cart))

                liste2 = []
                metin1 = ""

                for a in liste_n:
                    metin1 = metin1 + str(a)

                lite1 = metin1.split(',')

                kume1 = set()
                for t in lite1:
                    kume1.add(t)
                kume1 = list(kume1)
                yedek_kume1 = kume1
                datas1 = []
                for b in kume1:
                    datas1.append(lite1.count(b))
                datas_yedek = datas1

                print(datas1)
                try:
                    for l in range(5):
                        maxFind = max(datas1)
                        print(maxFind)
                        findIndex = datas1.index(maxFind)
                        findItemValue = datas1[findIndex]
                        findItem = kume1[findIndex]
                        veriler1.append(findItemValue)
                        etiketler1.append(findItem)
                        kume1.pop(findIndex)
                        datas1.pop(findIndex)
                except:
                    raise ValueError("Şu an için veri bulunmamakta")

                    # days = 7
                    # start_date = timezone.now().today() - datetime.timedelta(days=days - 1)
                    # new_labels = []
                    # new_datas = []
                    # datetime_liste = []
                    # for x in range(0, days):
                    #     new_t = start_date + datetime.timedelta(days=x)
                    #     datetime_liste.append(new_time)
                    #
                    #     new_labels.append(
                    #         new_time.strftime("%a")
                    #     )
                    #     new_q = new_carts.filter(updated_day=new_t.day, updated_month=new_t.month)
                    #     day_total = new_q.totals_data()["cart__products"] or 0
                    #     new_datas.append(
                    #         day_total
                    #     )

                data['labels'] = etiketler1
                data['data'] = veriler1
                data['ctip'] = 'bar'
                data['etiket'] = 'Satışlar(adet)'

        return JsonResponse(data)




class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return HttpResponse("İzin verilmedi", status=401)
            # return render(self.request, '400.html',{})

        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        print('asfafafafasfa', context)
        # two_week_ago = timezone.now() - datetime.timedelta(days=14)
        # now = timezone.now()
        # qs = Order.objects.all().by_range(start_date=two_week_ago, end_date=now)
        qs = Order.objects.all().by_weeks_range(weeks_ago=1, number_of_weeks=1)
        # start_date = timezone.now().date() - datetime.timedelta(hours=24)
        start_date = timezone.now() + datetime.timedelta(hours=3)
        start_date = start_date.date()
        # aa = timezone.now() - datetime.timedelta(days=28)
        # bb = timezone.now() - datetime.timedelta(days=21)
        # print(aa)
        # print(bb)
        print(start_date)
        # end_date = timezone.now().date() + datetime.timedelta(hours=12)
        end_date = timezone.now() + datetime.timedelta(hours=3)
        print(end_date)
        today_data = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
        context['today'] = today_data
        context['this_week'] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=4, number_of_weeks=1).get_sales_breakdown()
        # state_qs = Address.objects.filter(address_type="billing").aggregate(Count("state"))
        # state_qs_count = Address.objects.filter(state="buca").aggregate(Count("state"))
        # context['state'] = state_qs
        # context['state_count'] = state_qs_count
        # context['orders'] = qs
        # context['recent_orders'] = qs.recent().not_refunded()
        # context['recent_orders_data'] = context['recent_orders'].totals_data()
        # context['recent_orders_cart_data'] = context['recent_orders'].cart_data()
        # context['shipped_orders'] = qs.recent().not_refunded().by_status(status='shipped')
        # context['paid_orders'] = qs.recent().not_refunded().by_status(status='paid')
        # context['paid_orders_data'] = context['paid_orders'].totals_data()
        # context['shipped_orders_data'] = context['shipped_orders'].totals_data()
        return context

