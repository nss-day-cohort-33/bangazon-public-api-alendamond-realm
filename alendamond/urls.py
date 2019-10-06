from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapi.models import *
from bangazonapi.views import Customers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
from bangazonapi.views import register_user, login_user, Orders


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'orders', Orders, 'order')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth$', include('rest_framework.urls', namespace='rest_framework')),
]
