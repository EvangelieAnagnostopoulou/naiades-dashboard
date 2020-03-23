from naiades_dashboard.models import *


def add_meter_info(request):
    meter_info = None

    if request.user.is_authenticated:
        meter_info = MeterInfo.objects.filter(accesses__user=request.user).first()

    return {
       "meter_info": meter_info,
    }
