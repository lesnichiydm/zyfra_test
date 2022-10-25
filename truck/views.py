from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from truck.forms import TruckListFormSet, get_truck_list_for_calc_unload
from truck.services.forms import calc_warehouses_info_after_upload_mineral


class TruckListView(FormView):
    form_class = TruckListFormSet
    success_url = reverse_lazy("truck:calc_unload")
    template_name = "form.html"

    def get_initial(self, *args, **kwargs):
        return get_truck_list_for_calc_unload()

    def form_valid(self, form):
        self.request.session["last_calc_trucks"] = {
            i["truck_pk"]: i["unload_point"] for i in form.cleaned_data
        }
        return super().form_valid(form)


class CalcUnloadView(TemplateView):
    template_name = "calc_unload_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_calc = self.request.session.get("last_calc_trucks", {})
        context["warehouse_list"] = calc_warehouses_info_after_upload_mineral(
            self.request.session.get("last_calc_trucks", {})
        )
        return context
