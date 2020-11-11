import os
import random

from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Sum, Q, F, Count, DecimalField
from django.db.models.functions import TruncDate, Cast, ExtractDay
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from naiades_dashboard.models import Consumption, MeterInfoAccess, MeterInfo


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


def get_total_period_consumption_by_activity(qs, period_q):
    qs = qs.\
        filter(period_q).\
        annotate(name=F('meter_number__activity')).\
        values('name').\
        annotate(total_consumption=Sum('consumption'))

    qs = list(qs)

    return qs


def get_period_consumption_by_meter(qs, period_q):
    qs = qs. \
             filter(period_q). \
             values('meter_number'). \
             annotate(total_consumption=Sum('consumption')). \
             order_by('total_consumption')

    qs = list(qs)

    # fetch viewer's first name per meter number
    names_by_meter_number = {
        datum["meter_number"]: datum["first_name"]
        for datum in (
            MeterInfoAccess.objects.
            filter(meter_info__meter_number__in=[q["meter_number"] for q in qs], role='VIEWER').
            annotate(meter_number=F("meter_info__meter_number")).
            annotate(first_name=F("user__first_name")).
            values("meter_number", "first_name")
        )
    }
    for q in qs:
        q["name"] = names_by_meter_number.get(q['meter_number'], q['meter_number'])

    return qs


def get_period_change(qs, days, fn=get_period_consumption_by_meter):
    period_q = Q(date__gt=now().date() - timedelta(days=days)) & \
        Q(date__lte=now().date())

    last_period_q = Q(date__gt=now().date() - timedelta(days=days * 2)) & \
                  Q(date__lte=now().date() - timedelta(days=days))

    this_period_qs = fn(qs, period_q)
    last_period_qs = {
        datum["name"]: datum["total_consumption"]
        for datum in fn(qs, last_period_q)
    }

    qs = []
    for datum in this_period_qs:
        baseline = last_period_qs.get(datum["name"], 0)

        # we can not say how much it changed if last week was zero
        if not baseline:
            continue

        change = round((datum["total_consumption"] - baseline) / baseline * 100, 1)

        entry = {
            "increase" if change > 0 else "decrease": change,
            "this_period": datum["total_consumption"],
            "last_period": baseline,
            "change": change,
            "color": "#FF0F00" if change > 0 else "#04D215"
        }

        if "meter_number" in datum:
            entry.update({
                "meter_number": datum["meter_number"],
                "school": datum["name"],
            })
        else:
            entry.update({
                "name": datum["name"],
            })

        qs.append(entry)

    return sorted(qs, key=lambda datum: datum["change"])


def get_average_change(qs):
    try:
        return sum(datum["change"] for datum in qs) / len(qs)
    except ZeroDivisionError:
        return 0


def get_meter_infos(request):
    meter_infos = MeterInfo.objects.all()

    # filter by activity type
    if request.GET.get("activity"):
        meter_infos = meter_infos.filter(activity=request.GET["activity"])

    # text search
    if request.GET.get("q"):
        meter_infos = meter_infos.filter(meter_number__icontains=request.GET["q"])

    return JsonResponse({
        "meters": [
            meter_info.to_dict()
            for meter_info in meter_infos
        ]
    })


def get_measurement_data(request, metric, extra):
    dest = "naiades_dashboard" \
        if request.user.is_authenticated \
        else "city_dashboard"

    meter_info = MeterInfo.objects.filter(accesses__user=request.user).first() \
        if dest == "naiades_dashboard" \
        else None

    date = now().date()

    if os.environ.get("FIXED_DATE"):
        date = datetime(2020, 3, 21)

    qs = Consumption.objects.all()

    if dest == "naiades_dashboard":
        qs = qs.filter(is_school=True)

    week_q = Q(date__gt=date - timedelta(days=7)) & \
        Q(date__lte=date)

    # filter by activity
    if request.GET.get("activity"):
        qs = qs.filter(meter_number__activity=request.GET["activity"])

    # filter by meter id
    if request.GET.get("id"):
        qs = qs.filter(meter_number=request.GET["id"])

    if metric == "consumption":
        days = int(request.GET.get("days", "30"))
        days_offset = int(request.GET.get("days_offset", "0"))

        if meter_info:
            qs = qs.filter(meter_number=meter_info.meter_number)

        qs = qs.\
            filter(date__lt=now() - timedelta(days=days_offset)).\
            filter(date__gte=now() - timedelta(days=days + days_offset)).\
            annotate(mday=ExtractDay('date')).\
            values('year', 'month', 'mday', 'hour').\
            annotate(total_consumption=Sum('consumption')).\
            order_by().\
            order_by('year', 'month', 'mday', 'hour')

    elif metric == "total_hourly_consumption":
        qs = qs.\
            filter(meter_number=meter_info.meter_number).\
            values('hour').\
            order_by('hour').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "meter_daily_consumption":
        qs = qs. \
            filter(meter_number=request.GET.get("meter_number")). \
            filter(date__gt=now() - timedelta(days=365)).\
            annotate(date_grouped=TruncDate('date')).\
            values('date_grouped').\
            annotate(daily_consumption=Sum('consumption')).\
            order_by('date_grouped')

    elif metric == "avg_daily_consumption":

        # return hourly average consumption
        qs = qs.\
            filter(date__gt=now() - timedelta(days=365)).\
            annotate(date_grouped=TruncDate('date')).\
            values('date_grouped').\
            annotate(total_daily_consumption=Sum('consumption')).\
            annotate(n_meters=Count('meter_number', distinct=True, output_field=DecimalField())).\
            annotate(avg_daily_consumption=F('total_daily_consumption') / F('n_meters')).\
            order_by('date_grouped')

    elif metric == "total_daily_consumption":
        qs = qs. \
            filter(meter_number=meter_info.meter_number). \
            values('day').\
            order_by('day').\
            annotate(total_consumption=Sum('consumption'))

    elif metric == "weekly_consumption_by_meter":
        qs = get_period_consumption_by_meter(qs, period_q=week_q)

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

        # filter out too low consumptions
        # ignore schools with less than VS_OTHERS_MIN_LT_PER_MONTH lt/week
        if os.environ.get('VS_OTHERS_MIN_LT_PER_MONTH'):
            meter_totals = [
                datum
                for datum in meter_totals
                if datum['total_consumption'] >= float(os.environ.get('VS_OTHERS_MIN_LT_PER_MONTH'))
            ]

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
                if meter_info and datum['meter_number'] == meter_info.meter_number
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
        qs = get_period_change(qs, days=7)

    elif metric == "weekly_change_by_activity":
        qs = get_period_change(qs, days=7, fn=get_total_period_consumption_by_activity)

    elif metric == "yearly_change":
        qs = get_period_change(qs, days=365)

    elif metric == "yearly_change_by_activity":
        qs = get_period_change(qs, days=365, fn=get_total_period_consumption_by_activity)

    elif metric == "you_vs_others_weekly_change":
        data_qs = get_period_change(qs, days=7)

        top_20_qs = data_qs[:int(len(data_qs) / 5)]
        top_20 = get_average_change(top_20_qs)

        avg = get_average_change(data_qs)

        try:
            mine = [
                datum["change"]
                for datum in data_qs
                if datum["meter_number"] == MeterInfoAccess.objects.filter(user=request.user).first().meter_info_id
            ][0]
        except IndexError:
            mine = 0

        qs = [{
            "school": "Best 20%",
            "increase" if top_20 > 0 else "decrease": top_20,
            "change": top_20,
            "color": "#FF0F00" if top_20 > 0 else "#04D215"
        }, {
            "school": "Average",
            "increase" if avg> 0 else "decrease": avg,
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

    elif metric == "meter_info":
        return list(MeterInfo.objects.values("meter_number", "activity", "latitude", "longitude"))

    else:
        raise ValueError('Invalid metric: "%s"' % metric)

    return list(qs)


def measurement_data(request):
    return JsonResponse({
        "data": get_measurement_data(request=request, metric=request.GET.get('metric'), extra=request.GET)
    })
