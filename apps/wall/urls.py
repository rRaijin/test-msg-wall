from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^wall/$', Wall.as_view(), name='msg-wall'),
    url(r'^logout/$', logout, name="logout"),
    url(r'^', index, name='login'),
]