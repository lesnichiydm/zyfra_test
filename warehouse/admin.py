from django.contrib import admin

from .models import (OutsideWarehouseMoveMineralEvent, Warehouse,
                     WarehouseMoveMineralEvent)

admin.site.register(Warehouse)
admin.site.register(WarehouseMoveMineralEvent)
admin.site.register(OutsideWarehouseMoveMineralEvent)
