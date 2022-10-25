from django import forms
from django.core.validators import RegexValidator

from truck.services.base import (calc_truck_capacity_owerload_percent,
                                 get_not_complited_trips)


class TruckListForm(forms.Form):
    truck_pk = forms.CharField(
        widget=forms.HiddenInput(),
    )
    side_number = forms.CharField(
        label="бортовой номер",
        disabled=True,
        required=False,
    )
    model = forms.CharField(
        label="модель",
        disabled=True,
        required=False,
    )
    capacity = forms.CharField(
        label="макс. грузоподьемность",
        disabled=True,
        required=False,
    )
    weight_tons = forms.CharField(
        label="текущий вес",
        disabled=True,
        required=False,
    )
    owerload = forms.CharField(
        label="перегруз, %",
        disabled=True,
        required=False,
    )
    unload_point = forms.CharField(
        label="координаты разгрузки (x y)",
        validators=[RegexValidator(r"(\d+ \d+)", message="Формат X Y")],
    )

    def clean_unload_point(self):
        return tuple(map(float, self.cleaned_data["unload_point"].split()))


TruckListFormSet = forms.formset_factory(
    TruckListForm,
    extra=0,
)


def get_truck_list_for_calc_unload():
    """Получение списка загруженных рудой грузовиков
    в формате для инициализации формы"""
    return [
        {
            "truck_pk": i.truck.pk,
            "side_number": i.truck.side_number,
            "model": i.truck.model.name,
            "capacity": i.truck.capacity,
            "weight_tons": i.weight_tons,
            "owerload": calc_truck_capacity_owerload_percent(
                i.truck, i.weight_tons
            ),
        }
        for i in get_not_complited_trips()
    ]
