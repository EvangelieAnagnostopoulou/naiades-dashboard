from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from naiades_dashboard.models import MeterInfo
from social.models import *


def accept_tweets(modeladmin, request, queryset):
    cnt = queryset.update(is_accepted=True)

    messages.add_message(request, messages.SUCCESS, f'{cnt} tweet(s) marked as accepted.')


accept_tweets.short_description = _("Accept all selected tweets")


def reject_tweets(modeladmin, request, queryset):
    cnt = queryset.update(is_accepted=False)

    messages.add_message(request, messages.ERROR, f'{cnt} tweet(s) marked as rejected.')


reject_tweets.short_description = _("Reject all selected tweets")


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'message', 'is_accepted', 'is_deleted')
    list_filter = ('is_accepted', )
    search_fields = ('message', 'user', )

    actions = [accept_tweets, reject_tweets]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            meter_info = MeterInfo.objects.\
                filter(accesses__user=request.user).\
                first()

            qs = qs.filter(user__accesses__meter_info=meter_info)

        return qs
