from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from core.api import views as views
from . import auth_views
from rest_auth.views import LogoutView

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='index'),
    path('segmentation/', views.SegmentationView.as_view(), name='segmentation'),
    path('concordance/', views.ConcordanceView.as_view(), name='concordance'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', auth_views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/github/', auth_views.GithubLogin.as_view(), name='github_login'),
    path('rest-auth/facebook/', auth_views.GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/logout/', LogoutView.as_view(), name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)
