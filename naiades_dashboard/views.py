from datetime import timedelta

from django.db.models import Avg, Min, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from naiades_dashboard.models import Consumption


def leaderboard(request):
    return render(request, 'leaderboard.html')


def statistics(request):
    return render(request, 'statistics.html')


def get_measurement_data(metric, extra):
    qs = Consumption.objects.all()

    if metric == "total_hourly_consumption":
        qs = qs.\
            values('hour').\
            order_by('hour').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "total_daily_consumption":
        qs = qs.\
            values('day').\
            order_by('day').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "weekly_consumption_by_meter":
        qs = qs.\
            values('meter_number', 'activity').\
            annotate(total_consumption=Sum('consumption')).\
            order_by('total_consumption')[:10]

    elif metric == "you_vs_others":
        data_qs = qs.\
            filter(date__gte=now().date() - timedelta(days=7))

        n_meters = data_qs.values('meter_number').distinct().count()

        # top 20%
        n_top_20 = int(n_meters / 5)

        try:
            top_20 = (data_qs.\
                values('meter_number').\
                annotate(total=Sum('consumption')).\
                order_by('total')[:n_top_20].\
                aggregate(overall_total=Sum('total'))['overall_total'] or 0) / n_top_20
        except ZeroDivisionError:
            top_20 = 0

        # average
        try:
            avg = (data_qs.aggregate(total=Sum('consumption'))['total'] or 0) / n_meters
        except ZeroDivisionError:
            avg = 0

        # your school
        your = data_qs.\
            filter(meter_number=Consumption.objects.all().first().meter_number).\
            aggregate(total=Sum('consumption'))['total'] or 0

        qs = [
            {"entity": "Best 20%", "weekly_total": top_20},
            {"entity": "Average", "weekly_total": avg},
            {"entity": "Your school", "weekly_total": your},
        ]

    elif metric == "all":
        qs = qs.\
            values('meter_number', 'latitude', 'longitude'). \
            annotate(total_consumption=Sum('consumption'))[:50]

    else:
        raise ValueError('Invalid metric: "%s"' % metric)

    return list(qs)


def measurement_data(request):
    return JsonResponse({
        "data": get_measurement_data(metric=request.GET.get('metric'), extra=request.GET)
    })
