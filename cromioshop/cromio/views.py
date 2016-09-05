from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.http import Http404

from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.models import Order
from plata.shop.views import Shop

from cromio.models import Product, OrderWithData


# Create your views here.
shop = Shop(
    contact_model=Contact,
    order_model=OrderWithData,
    discount_model=Discount,
)

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(label=_('Quantity'), initial=1,
        min_value=1, max_value=100)

    material = forms.ChoiceField(label=_('Material'), choices=[])
    size = forms.ChoiceField(label=_('Size'), choices=[])


    def __init__(self, product, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)

        config = product.get_config()
        sizes = list(set([x[1] for x in config]))
        materials = list(set([x[0] for x in config]))

        #todo: we should lookup in materials model
        self.fields['material'] = forms.ChoiceField(
            choices=[(str(o), str(o)) for o in materials]
        )
        self.fields['size'] = forms.ChoiceField(
            choices=[(str(o), str(o)) for o in sizes]
        )


class ProductDetailView(FormView):
    template_name = "product_detail.html"
    #form_class = OrderItemForm
    success_url = reverse_lazy('plata_shop_cart')


    def get_form(self, form_class=None):
        return OrderItemForm(self.product, **self.get_form_kwargs())

    def dispatch(self, request, *args, **kwargs):
        try:
            self.product = Product.objects.get(slug = self.kwargs.get('product_slug'))
        except Product.DoesNotExist:
            raise Http404("product does not exist")

        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        #product = Product.objects.get(slug = self.kwargs.get('product_slug'))
        context['product'] = self.product
        return context

    def form_valid(self, form):
        product = Product.objects.get(slug = self.kwargs.get('product_slug'))
        order = shop.order_from_request(self.request, create=True)
        size = form.cleaned_data.get('size')

        material = form.cleaned_data.get('material')
        print "aa", size, material

        try:
            order.modify_item(
                product,
                absolute=form.cleaned_data.get('quantity'),
                data = { "size" : size, "material" : material},
                force_new=True)
            #messages.success(request, _('The cart has been updated.'))
        except ValidationError, e:
            raise
            if e.code == 'order_sealed':
                [messages.error(request, msg) for msg in e.messages]
            else:
                raise

        return super(ProductDetailView, self).form_valid(form)
