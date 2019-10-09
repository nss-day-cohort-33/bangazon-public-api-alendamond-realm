from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapi.models import *
from bangazonapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'orders', Orders, 'order')
router.register(r'products', ProductData, 'product')
router.register(r'producttypes', ProductTypes, 'producttype')
router.register(r'users', Users, 'user')
router.register(r'customers', Customers, 'customer')
router.register(r'orderproduct', OrdersProducts, 'orderproduct')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth$', include('rest_framework.urls', namespace='rest_framework')),
]
