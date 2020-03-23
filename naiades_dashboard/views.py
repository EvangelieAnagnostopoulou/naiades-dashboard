import random

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Sum, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from naiades_dashboard.models import Consumption, MeterInfoAccess


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
        try:
            q['name'] = MeterInfoAccess.objects.\
                get(meter_info__meter_number=q['meter_number'], role='VIEWER').\
                user.first_name
        except MeterInfoAccess.DoesNotExist:
            q['name'] = q['meter_number']

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
    qs = Consumption.objects.filter(meter_number__activity='School')
    week_q = Q(date__gt=now().date() - timedelta(days=7)) & \
        Q(date__lte=now().date())

    if metric == "total_hourly_consumption":
        qs = qs.\
            filter(meter_number=request.user.meter_info.meter_number).\
            values('hour').\
            order_by('hour').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "total_daily_consumption":
        qs = qs. \
            filter(meter_number=request.user.meter_info.meter_number). \
            values('day').\
            order_by('day').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "weekly_consumption_by_meter":
        qs = get_weekly_consumption_by_meter(qs, week_q)

    elif metric == "you_vs_others":
        data_qs = qs.\
            filter(week_q)

        # get meter totals
        meter_totals = [
            datum
            for datum in data_qs.\
                values('meter_number').\
                annotate(total_consumption=Sum('consumption'))
            if (datum['total_consumption'] or 0) > 0
        ]

        # sort from smallest to largest
        meter_totals = sorted(meter_totals, key=lambda datum: datum['total_consumption'])

        # top 20%
        n_top_20 = int(len(meter_totals) / 5)

        try:
            top_20 = sum([datum['total_consumption'] for datum in meter_totals[:n_top_20]]) / n_top_20
        except ZeroDivisionError:
            top_20 = 0

        # average
        try:
            avg = sum([datum['total_consumption'] for datum in meter_totals]) / len(meter_totals)
        except ZeroDivisionError:
            avg = 0

        # your school
        try:
            your = [
                datum['total_consumption']
                for datum in meter_totals
                if datum['meter_number'] == request.user.meter_info.meter_number
            ][0]
        except IndexError:
            your = 0

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
            {"month": "March 2018", "consumption": 120, "color": "#04D215"},
            {"month": "March 2019", "consumption": 80, "color": "#F8FF01"}
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
