from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from carts.models import Cart
from .models import Product
from tags.models import Tag
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"


    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Product.objects.all().featured()

class ProductFeaturedDeatilView(ObjectViewedMixin,DetailView): #ObjectViewedMixin,
    queryset = Product.objects.featured()
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Product.objects.all().featured()

class UserProductHistoryView(LoginRequiredMixin,ListView):
    # template_name = "products/user-history.html"
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=True) #.filter(content_type__name='product')
        # viewed_ids = [x.object_id for x in views]
        # Product.objects.filter(pk__in=viewed_ids)
        return views


class ProductListView(ListView):
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # tag = Tag.objects.get(title='çorba')
        # tag2 = Tag.objects.get(title='tatlı')
        # return tag.products.all()
        return Product.objects.all()



# def product_list_view(request):
#     tag = Tag.objects.get(title='çorba')
#     a = tag.products.all()
#     # tag_queryset = Tag.objects.get_queryset()
#     # for tag_obj in tag_queryset:
#     #     obj = tag_obj.products.all()
#
#     queryset = Product.objects.all()
#     # tag_query_set = Tag.objects.all()
#     # corba_set = Tag.objects.get(title='çorba')
#
#
#     context = {
#         'object_list': 'a',
#         # 'tag_list':tag_query_set,
#         # 'corba_list': corba_set
#         # 'corba_list': a
#
#     }

    # return render(request, 'products/list.html', {})


class ProductDetailSlugView(ObjectViewedMixin, DetailView): #ObjectViewedMixin,
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Bulunamadı..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Garip bir istek..")

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)

        return instance

class ProductDetailView(ObjectViewedMixin, DetailView): #ObjectViewedMixin,
    # queryset = Product.objects.all()
    template_name = "products/detail.html"
    def get_context_data(self, *args, **kwargs):

        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context


    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Ürün mecvut eğil")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #
    #     return Product.objects.filter(pk=pk)



def product_detail_view(request, pk=None, *args, **kwargs ):
    # instance = Product.objects.get(pk=pk, featured=True)
    # instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     instance = Product.objects.get(id=pk)
    #
    # except Product.DoesNotExist:
    #     raise Http404("Ürün mecvut eğil")
    #
    # except:
    #     print("NOpe")

    instance = Product.objects.get_by_id(pk)

    if instance is None:
        raise Http404("Ürün mecvut eğil")

    # print(instance)
    #
    # qs = Product.objects.filter(id=pk)
    #
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Ürün mecvut eğil")

    context = {
        'object': instance

        }

    return render(request, 'products/detail.html', context)
