import locale
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from carts.models import CartItem
from orders.models import Order
from django.utils import timezone
try:
    locale.setlocale(locale.LC_ALL, "tr")
except locale.Error:
    pass

class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            liste = []
            if request.GET.get('type') == 'product':


                proList = []
                for p in CartItem.objects.raw('''SELECT *, SUM(quantity) AS deger FROM carts_cartitem GROUP BY carts_cartitem.product_id ORDER BY deger DESC'''):
                    proList.append([p.deger, p.product.title])
                # proList = sorted(proList, reverse=True)

                veriler = []
                etiketler = []
                sayac = 0
                for i in proList:
                    if sayac < 5:
                        veriler.append(i[0])
                        etiketler.append(i[1])
                        sayac += 1
                    else:
                        pass

                data['labels'] = etiketler[:5]
                data['data'] = veriler[:5]
                data['ctip'] = 'bar'
                data['etiket'] = 'Satışlar(Adet)'
        return JsonResponse(data)
class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return HttpResponse("İzin verilmedi", status=401)
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        print('asfafafafasfa', context)
        qs = Order.objects.all().by_weeks_range(weeks_ago=1, number_of_weeks=1)
        start_date = timezone.now() + datetime.timedelta(hours=3)
        start_date = start_date.date()
        print(start_date)
        end_date = timezone.now() + datetime.timedelta(hours=3)
        print(end_date)
        today_data = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
        context['today'] = today_data
        context['this_week'] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=4, number_of_weeks=1).get_sales_breakdown()
        return context

