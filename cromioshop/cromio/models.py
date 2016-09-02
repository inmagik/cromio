from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from plata.product.models import ProductBase
from plata.shop.models import PriceBase


class Product(ProductBase):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('plata_product_detail', (), {'slug': self.slug})

class ProductPrice(PriceBase):
    product = models.ForeignKey(Product, verbose_name=_('product'),
        related_name='prices')

    class Meta:
        get_latest_by = 'id'
        ordering = ['-id']
        verbose_name = _('price')
        verbose_name_plural = _('prices')
