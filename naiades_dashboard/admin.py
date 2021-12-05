from django.contrib import admin
from django.db.models import F

from naiades_dashboard.models import (
    MeterInfo,
    MeterInfoAccess,
    Consumption,
)


@admin.register(MeterInfo)
class MeterInfoAdmin(admin.ModelAdmin):
    search_fields = ("meter_number", )
    list_display = ("meter_number", "activity", "address", "size", "service_point_id", "service_connection_id", )
    list_filter = ("activity", )


@admin.register(MeterInfoAccess)
class MeterInfoAccessAdmin(admin.ModelAdmin):
    search_fields = ("meter_info__meter_number", )
    list_display = ("meter_info", "user", "role", )


@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    search_fields = ("meter_number_id__meter_number", )
    list_display = ("meter_number_id", "consumption", "date", "hour", "estimated", )
    ordering = ("-date", "-hour", )
    raw_id_fields = ("meter_number_id", )

    def get_queryset(self, request):
        return super().\
            get_queryset(request).\
            annotate(meter_number_id_str=F("meter_number_id"))
