from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views as views

app_name = 'api'

urlpatterns = [
    re_path(r'^segment/$', views.segment, name='segment'),
    re_path(r'^concordance/$', views.concordance, name='concordance'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
