from django.contrib import admin

from naiades_dashboard.models import (
    MeterInfo,
    MeterInfoAccess,
    Consumption,
)


@admin.register(MeterInfo)
class MeterInfoAdmin(admin.ModelAdmin):
    list_display = ("meter_number", "activity", "address", "service_point_id", "service_connection_id", )
    list_filter = ("activity", )


@admin.register(MeterInfoAccess)
class MeterInfoAccessAdmin(admin.ModelAdmin):
    list_display = ("meter_info", "user", "role", )


@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ("meter_number_id", "consumption", "date", "hour", "estimated", )
    ordering = ("-date", "-hour", )
