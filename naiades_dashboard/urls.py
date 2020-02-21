from django.urls import path

from naiades_dashboard import views


urlpatterns = [
    # api
    path('api/measurements/data', views.measurement_data, name='measurement-data'),

    # pages
    path('', views.leaderboard, name='leaderboard'),
    path('statistics', views.statistics, name='statistics'),
    path('reduction', views.reduction, name='reduction'),
    path('consumption', views.consumption, name='consumption'),
]
