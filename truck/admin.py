from django.contrib import admin

from .models import TripTruck, Truck, TruckModel

admin.site.register(Truck)
admin.site.register(TruckModel)
admin.site.register(TripTruck)
