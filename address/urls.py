"""address URL Configuration

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
from django.urls import path

from housePrice import views

urlpatterns = [
    path('home/', views.homePage),
    path('forecast/', views.houseForecast),
    path('admin/', admin.site.urls),
    path('test/', views.empty_test_page),
    path('list/', views.list_),
    path('location/', views.get_house_location),
    path('lat/', views.baiduLNTLat),
    path('jijian/', views.baiduConstruction),
    path('test_ajax/', views.ajax_post),
    path('pmc/', views.getConInfo),
    path('detail/<int:id>/', views.skipInfo, name='detail_info'),
    path('refer/', views.referInfo),
    path('listSFUN/', views.listSFUN),
]
handler500 = "housePrice.views.server_error"
