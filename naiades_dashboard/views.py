from django.db.models import Avg, Min, Sum
from django.http import JsonResponse
from django.shortcuts import render

from naiades_dashboard.models import Consumption


def dashboard(request):
    return render(request, 'dashboard.html')


def get_measurement_data(metric):
    qs = Consumption.objects.all()

    if metric == "total_hourly_consumption":
        qs = qs.\
            values('hour').\
            order_by('hour').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "total_daily_consumption":
        qs = qs.\
            values('day').\
            annotate(min_counter=Min('hour_idx')).\
            order_by('min_counter').\
            annotate(total_consumption=Sum('consumption'))

    else:
        raise ValueError('Invalid metric: "%s"' % metric)

    return list(qs)


def measurement_data(request):
    return JsonResponse({
        "data": get_measurement_data(metric=request.GET.get('metric'))
    })
