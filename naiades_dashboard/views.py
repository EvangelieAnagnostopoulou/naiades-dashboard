from django.db.models import Avg, Min, Sum
from django.http import JsonResponse
from django.shortcuts import render

from naiades_dashboard.models import Consumption


def dashboard(request):
    return render(request, 'dashboard.html')


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
