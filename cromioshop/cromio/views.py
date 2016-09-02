from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.models import Order
from plata.shop.views import Shop

from cromio.models import Product


# Create your views here.
shop = Shop(
    contact_model=Contact,
    order_model=Order,
    discount_model=Discount,
)

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(label=_('quantity'), initial=1,
        min_value=1, max_value=100)

class ProductDetailView(FormView):
    template_name = "product_detail.html"
    form_class = OrderItemForm
    success_url = reverse_lazy('plata_shop_cart')

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = Product.objects.get(slug = self.kwargs.get('product_slug'))
        context['product'] = product
        return context

    def form_valid(self, form):
        product = Product.objects.get(slug = self.kwargs.get('product_slug'))
        order = shop.order_from_request(self.request, create=True)
        try:
            order.modify_item(product, form.cleaned_data.get('quantity'))
            #messages.success(request, _('The cart has been updated.'))
        except ValidationError, e:
            raise
            if e.code == 'order_sealed':
                [messages.error(request, msg) for msg in e.messages]
            else:
                raise

        return super(ProductDetailView, self).form_valid(form)
