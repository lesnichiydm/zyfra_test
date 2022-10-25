from django.urls import include, path

from truck.views import CalcUnloadView, TruckListView

app_name = "truck"

urlpatterns = [
    path("", TruckListView.as_view(), name="trip_truck_calc_list"),
    path("calc/", CalcUnloadView.as_view(), name="calc_unload"),
]
