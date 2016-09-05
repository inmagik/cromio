from __future__ import unicode_literals
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from plata.product.models import ProductBase
from plata.shop.models import PriceBase, Order
from django.db.models import F, ObjectDoesNotExist, Sum
from django.core.exceptions import ValidationError

logger = logging.getLogger('__name__')

#REIMPLEMENTATION OF modify_item, see https://github.com/matthiask/plata/issues/78
class OrderWithData(Order):

    def modify_item(self, product, relative=None, absolute=None,
                    recalculate=True, data=None, item=None, force_new=False):
        """
        Updates order with the given product
        - ``relative`` or ``absolute``: Add/subtract or define order item
          amount exactly
        - ``recalculate``: Recalculate order after cart modification
          (defaults to ``True``)
        - ``data``: Additional data for the order item; replaces the contents
          of the JSON field if it is not ``None``. Pass an empty dictionary
          if you want to reset the contents.
        - ``item``: The order item which should be modified. Will be
          automatically detected using the product if unspecified.
        - ``force_new``: Force the creation of a new order item, even if the
          product exists already in the cart (especially useful if the
          product is configurable).
        Returns the ``OrderItem`` instance; if quantity is zero, the order
        item instance is deleted, the ``pk`` attribute set to ``None`` but
        the order item is returned anyway.
        """

        assert (relative is None) != (absolute is None),\
            'One of relative or absolute must be provided.'
        assert not (force_new and item),\
            'Cannot set item and force_new at the same time.'

        if self.is_confirmed():
            raise ValidationError(
                _('Cannot modify order once it has been confirmed.'),
                code='order_sealed')

        if item is None and not force_new:
            try:
                item = self.items.get(product=product)
            except self.items.model.DoesNotExist:
                # Ok, product does not exist in cart yet.
                pass
            except self.items.model.MultipleObjectsReturned:
                # Oops. Product already exists several times. Stay on the
                # safe side and add a new one instead of trying to modify
                # another.
                if not force_new:
                    raise ValidationError(
                        _(
                            'The product already exists several times in the'
                            ' cart, and neither item nor force_new were'
                            ' given.'),
                        code='multiple')

        if item is None:
            item = self.items.model(
                order=self,
                product=product,
                quantity=0,
                currency=self.currency,
            )

        if relative is not None:
            item.quantity += relative
        else:
            item.quantity = absolute

        if data is not None:
            item.data = data

        if item.quantity > 0:
            try:
                price = product.get_price(
                    currency=self.currency,
                    orderitem=item)
            except ObjectDoesNotExist:
                logger.error(
                    u'No price could be found for %s with currency %s' % (
                        product, self.currency))

                raise ValidationError(
                    _('The price could not be determined.'),
                    code='unknown_price')

            price.handle_order_item(item)
            product.handle_order_item(item)
            item.save()
        else:
            if item.pk:
                item.delete()
                item.pk = None

        if recalculate:
            self.recalculate_total()

            # Reload item instance from DB to preserve field values
            # changed in recalculate_total
            if item.pk:
                item = self.items.get(pk=item.pk)

        try:
            self.validate(self.VALIDATE_BASE)
        except ValidationError:
            if item.pk:
                item.delete()
            raise

        return item


class Support(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    #price in EUR
    price = models.FloatField()

class Product(ProductBase):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    configurations = models.TextField(_('configurations'), blank=True)
    accessories =  models.TextField(_('accessories'), blank=True)


    def get_config(self):
        lines = self.configurations.split("\r\n")
        lines = [x for x in lines if x]
        pieces = [x.split("|") for x in lines]
        print pieces
        return pieces

    class Meta:
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('plata_product_detail', (), {'slug': self.slug})


    def get_price(self, currency=None, orderitem=None):
        """
        This method is part of the public, required API of products. It returns
        either a price instance or raises a ``DoesNotExist`` exception.
        If you need more complex pricing schemes, override this method with
        your own implementation.
        """
        if currency is None:
            currency = (
                orderitem.currency if orderitem else
                plata.shop_instance().default_currency())

        try:
            return self.prices.get(
                currency=currency,
                size=orderitem.data.get('size', None),
                material=orderitem.data.get('material', None))

        except IndexError:
            raise self.prices.model.DoesNotExist

    def handle_order_item(self, orderitem):
        support_slug = orderitem.data.get('support', None)
        if support_slug:
            support_item = Support.objects.get(slug=support_slug)
            orderitem._unit_price += support_item.price

        orderitem.name = unicode(self)
        orderitem.sku = getattr(self, 'sku', '')

class ProductPrice(PriceBase):
    product = models.ForeignKey(Product, verbose_name=_('product'),
        related_name='prices')

    material = models.CharField(max_length=300, null=True, blank=True)
    size = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        get_latest_by = 'id'
        ordering = ['-id']
        verbose_name = _('price')
        verbose_name_plural = _('prices')

    
