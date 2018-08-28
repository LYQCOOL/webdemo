"""webdemo URL Configuration

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
# from django.urls import path
from app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index-(?P<nid>\d+)/',views.index),
    # url(r'^goods/', views.goods),
    url(r'^register/',views.register),
    url(r'^login/',views.login),
    url(r'check_code.html/',views.check_code),
    url(r'shoppingcar/',views.shoppingcar),
    # url(r'shopcar/',views.shopcar),
    url(r'shopping-car/',views.shopcar),
    url(r'logout/',views.logout),
    url(r'^sousuo/',views.sousuo),
    url(r'^index-sousuo/',views.sousuo_index),
    url(r'^information/',views.information),
    url(r'^pwd/', views.pwd),
    url(r'clean/',views.clean),
    url(r'order/',views.order),
    url(r'goumai/',views.goumai),
]
