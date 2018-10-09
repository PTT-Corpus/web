from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views as views

app_name = 'api'

urlpatterns = [
    re_path(r'^segment/$', views.SegmentationView.as_view(), name='segment'),
    re_path(r'^concordance/$', views.ConcordanceView.as_view(), name='concordance'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
