from django.conf.urls import url, include
from .views import HomePageView, ProductDetailView

urlpatterns = [

    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^products/(?P<product_slug>[\w-]+)/$', ProductDetailView.as_view(), name="product-detail"),

]
