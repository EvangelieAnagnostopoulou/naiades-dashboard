import random

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Sum, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from naiades_dashboard.models import Consumption


@login_required
def leaderboard(request):
    return render(request, 'leaderboard.html')


@login_required
def statistics(request):
    return render(request, 'statistics.html')


@login_required
def reduction(request):
    return render(request, 'reduction.html')


@login_required
def consumption(request):
    return render(request, 'consumption.html')


@login_required
def report(request):
    return render(request, 'report.html')


def get_weekly_consumption_by_meter(qs, week_q):
    qs = qs. \
             filter(week_q). \
             values('meter_number'). \
             annotate(total_consumption=Sum('consumption')). \
             order_by('total_consumption')

    qs = list(qs)
    for q in qs:
        q['name'] = User.objects.get(username=q['meter_number']).first_name

    return qs


def get_weekly_change(qs, week_q=None):
    if not week_q:
        week_q = Q(date__gt=now().date() - timedelta(days=7)) & \
            Q(date__lte=now().date())

    last_week_q = Q(date__gt=now().date() - timedelta(days=14)) & \
                  Q(date__lte=now().date() - timedelta(days=7))

    this_week_qs = get_weekly_consumption_by_meter(qs, week_q)
    last_week_qs = {
        datum["name"]: datum["total_consumption"]
        for datum in get_weekly_consumption_by_meter(qs, last_week_q)
    }

    qs = []
    for datum in this_week_qs:
        baseline = last_week_qs.get(datum["name"], 0)

        # we can not say how much it changed if last week was zero
        if not baseline:
            continue

        change = round((datum["total_consumption"] - baseline) / baseline * 100, 1)

        qs.append({
            "school": datum["name"],
            "increase" if change > 0 else "decrease": change,
            "change": change,
            "color": "#FF0F00" if change > 0 else "#04D215"
        })

    return sorted(qs, key=lambda datum: datum["change"])


def get_average_change(qs):
    return sum(datum["change"] for datum in qs) / len(qs)


def get_measurement_data(request, metric, extra):
    qs = Consumption.objects.all()
    week_q = Q(date__gt=now().date() - timedelta(days=7)) & \
        Q(date__lte=now().date())

    if metric == "total_hourly_consumption":
        qs = qs.\
            filter(meter_number=request.user.username).\
            values('hour').\
            order_by('hour').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "total_daily_consumption":
        qs = qs. \
            filter(meter_number=request.user.username). \
            values('day').\
            order_by('day').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "weekly_consumption_by_meter":
        qs = get_weekly_consumption_by_meter(qs, week_q)

    elif metric == "you_vs_others":
        data_qs = qs.\
            filter(week_q)

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
            filter(meter_number=request.user.username).\
            aggregate(total=Sum('consumption'))['total'] or 0

        qs = [
            {"entity": "Best 20%", "weekly_total": top_20, "color": "#04D215"},
            {"entity": "Average", "weekly_total": avg, "color": "#F8FF01"},
            {"entity": "My school", "weekly_total": your, "color": "#FF9E01"},
        ]

    elif metric == "message":
        if random.randint(0, 1) == 0:
            qs = [{
                'message': 'You ranked in the top 20%. Keep up the good work!!',
                'type': 'SUCCESS'
            }]
        else:
            qs = [{
                'message': 'Try more to reduce your consumption!',
                'type': 'FAILURE'
            }]

    elif metric == "weekly_change":
        qs = get_weekly_change(qs, week_q=week_q)

    elif metric == "you_vs_others_weekly_change":
        data_qs = get_weekly_change(qs, week_q=week_q)

        top_20_qs = data_qs[:int(len(data_qs) / 5)]
        top_20 = get_average_change(top_20_qs)

        avg = get_average_change(data_qs)
        mine = [datum["change"] for datum in data_qs if datum["school"] == request.user.first_name][0]

        qs = [{
            "school": "Best 20%",
            "increase" if top_20 > 0 else "decrease": top_20,
            "change": top_20,
            "color": "#FF0F00" if top_20 > 0 else "#04D215"
        }, {
            "school": "Average",
            "increase" if avg > 0 else "decrease": avg,
            "change": avg,
            "color": "#FF0F00" if avg > 0 else "#04D215"
        }, {
            "school": "My school",
            "increase" if mine > 0 else "decrease": mine,
            "change": mine,
            "color": "#FF0F00" if mine > 0 else "#04D215"
        }]

    elif metric == "monthly_consumption":
        qs = [
            {"month": "December 2018", "consumption": 120, "color": "#04D215"},
            {"month": "December 2019", "consumption": 80, "color": "#F8FF01"}
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
        "data": get_measurement_data(request=request, metric=request.GET.get('metric'), extra=request.GET)
    })
