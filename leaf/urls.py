from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^(?P<url>.*)$', views.page_detail),
)