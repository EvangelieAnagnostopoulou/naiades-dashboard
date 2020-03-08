from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from social.models import Tweet


@login_required
def show_feed(request):
    return render(request, 'social/feed.html')


@login_required
def get_tweets(request):
    max_tweets = 50
    tweets_qs = Tweet.objects.\
        exclude(is_deleted=True).\
        order_by().\
        order_by('-created')

    return JsonResponse({
        'tweets': [
            tweet.to_dict()
            for tweet in tweets_qs[:max_tweets]
        ]
    })


@login_required
def post_tweet(request):
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid method: only POST is allowed.',
        }, status=400)

    # validate data
    message = request.POST.get('message')

    if not message:
        return JsonResponse({
            'error': 'Message can not be empty.',
        }, status=400)

    # create the tweet
    tweet = Tweet.objects.create(
        user=request.user,
        message=message
    )

    # return its json representation
    return JsonResponse({
        'tweet': tweet.to_dict(),
    }, status=201)


@login_required
def update_tweet(request, tweet_id):
    # get tweet by ID
    # deleted tweets, or tweets posted by other users, can not be updated
    tweet = Tweet.objects.\
        filter(id=tweet_id, user=request.user, is_deleted=False).\
        first()

    if not tweet:
        return JsonResponse({
            'error': 'Tweet does not exist.',
        }, status=404)

    # validate
    message = request.POST.get('message')

    if not message:
        return JsonResponse({
            'error': 'Message can not be empty.',
        }, status=400)

    # update
    tweet.message = message
    tweet.save()

    # return updated tweet
    return JsonResponse({
        'tweet': tweet.to_dict(),
    }, status=20)


@login_required
def delete_tweet(request, tweet_id):
    # get tweet by ID
    # deleted tweets, or tweets posted by other users, can not be deleted
    tweet = Tweet.objects.\
        filter(id=tweet_id, user=request.user, is_deleted=False).\
        first()

    if not tweet:
        return JsonResponse({
            'error': 'Tweet does not exist.',
        }, status=404)

    # mark as deleted
    tweet.is_deleted = True
    tweet.save()

    # return empty response
    return JsonResponse({}, status=204)
