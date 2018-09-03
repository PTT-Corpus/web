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
from django.contrib.auth import views
import core.views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'auth/', include('social_django.urls', namespace='social')),
    path(r'', core.views.home, name='home'),
    path(r'index', core.views.index, name='index'),
    path(r'apidoc', core.views.apidoc, name='apidoc'),
    path(r'collocation', core.views.collocation, name='collocation'),
    path(r'concordance', core.views.concordance, name='concordance'),
    path(r'segmentation', core.views.segmentation, name='segmentation'),
    path(r'sentipol', core.views.sentipol, name='sentipol'),
    path(r'wordcloud', core.views.wordcloud, name='wordcloud'),
]
