from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^wall/$', Wall.as_view(), name='msg-wall'),

    url(r'^message/$', AddMessage.as_view(), name='add-message'),
    url(r'^message/edit/(?P<id>\d+)/$', EditMessage.as_view(), name='edit-message'),

    url(r'^comment/(?P<id>\d+)/(?P<pk>\d+)/$', AddComment.as_view(), name='add-comment'),
    url(r'^comment/edit/(?P<id>\d+)/$', EditComment.as_view(), name='edit-comment'),

    url(r'^logout/$', logout, name="logout"),
    url(r'^', index, name='login'),
]