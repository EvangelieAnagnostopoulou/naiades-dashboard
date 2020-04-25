from django.urls import path

from social import views


urlpatterns = [
    # api
    path('tweets/', views.get_tweets, name='get-tweets'),
    path('tweets/create/', views.post_tweet, name='post-tweet'),

    # pages
    path('feed', views.show_feed, name='feed'),
]
