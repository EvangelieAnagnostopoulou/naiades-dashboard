"""Project URL Configuration

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

from django.urls import path, include

from django.contrib import admin
import django.contrib.auth.views as auth_views

from .views import test_home
from naiades_dashboard import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('admin/', include('loginas.urls')),

    # api
    path('api/measurements/data', views.measurement_data, name='measurement-data'),

    # pages
    path('', views.leaderboard, name='leaderboard'),
    path('statistics', views.statistics, name='statistics'),
]
