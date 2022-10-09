from django.urls import path

from naiades_dashboard import views


urlpatterns = [
    # api
    path('api/measurements/data', views.measurement_data, name='measurement-data'),
    path('api/meters', views.get_meter_infos, name='meter-infos'),
    path('api/device-alerts', views.get_device_alerts, name='device-alerts'),

    # pages
    path('', views.leaderboard, name='leaderboard'),
    path('statistics', views.statistics, name='statistics'),
    path('reduction', views.reduction, name='reduction'),
    path('consumption', views.consumption, name='consumption'),
    path('report', views.report, name='report'),
    path('faq', views.faq, name='faq'),
]
