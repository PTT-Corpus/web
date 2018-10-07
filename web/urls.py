"""web URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path, include
import core.views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path(r'login/', views.login, name='login'),
    # path(r'logout/', views.logout, name='logout'),
    path(r'accounts/', include('allauth.urls')),
    path(r'', core.views.index, name='index'),
    path(r'api/', include('core.api_urls', namespace='api')),
    path(r'apidoc', core.views.apidoc, name='apidoc'),
    path(r'collocation', core.views.collocation, name='collocation'),
    path(r'concordance', core.views.ConcordanceFormView.as_view(), name='concordance'),
    path(r'segmentation', core.views.SegmentationFormView.as_view(), name='segmentation'),
    path(r'sentipol', core.views.sentipol, name='sentipol'),
    path(r'wordcloud', core.views.wordcloud, name='wordcloud'),
]
