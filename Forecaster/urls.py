"""Forecaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web.views import hello
from web.views import passval
from web.views import main
from web.views import predict
admin.autodiscover()

urlpatterns = [                 
    # here we are not using pattern module like in previous django versions
    url(r'^admin/', admin.site.urls),
    url(r'^hello/',hello),
    url(r'^$',main),
    url(r'^predict/',predict),
]
