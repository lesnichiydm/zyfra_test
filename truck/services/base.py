from typing import Union

from django.contrib.gis.geos import Point
from django.utils import timezone

from extraction_point.models import ExtractionPoint
from truck.models import TripTruck, Truck, TruckModel
from warehouse.models import (
    OutsideWarehouseMoveMineralEvent,
    WarehouseMoveMineralEvent,
)
from warehouse.services.base import (
    unload_mineral_to_outside_warehouse,
    unload_mineral_to_warehouse,
)
from warehouse.services.geo import get_warehouse_by_geo_point


def add_truck_model_if_not_exist(
    name: str,
    capacity: int,
) -> TruckModel:
    """Создание модели самосвала"""
    return TruckModel.objects.get_or_create(
        name=name,
        capacity=capacity,
    )[0]


def add_truck(side_number: str, model: TruckModel) -> Truck:
    """Создание самосвала"""
    return Truck.objects.create(
        side_number=side_number,
        model=model,
    )


def add_truck_with_model(
    side_number: str,
    model_name: str,
    capacity: int,
) -> Truck:
    """Упрощенное создание самосвала вместе его моделью"""
    model = add_truck_model_if_not_exist(model_name, capacity)
    return add_truck(side_number, model)


def calc_truck_capacity_owerload_percent(
    truck: Truck,
    weight_tons: int,
) -> int:
    """Рассчет перегруза самосвала"""
    ower_percent = int((weight_tons - truck.capacity) * 100 / truck.capacity)
    return ower_percent if ower_percent > 0 else 0


def add_mineral_to_truck(
    truck: Truck, extraction_point: ExtractionPoint, weight_tons: int
) -> bool:
    """Создание события загрузки руды в самосвал"""
    if get_truck_current_trip(truck):
        # Впринципе ничего не мешает в этой логике
        # догружать в самосвал с нескольких точек
        # но думаю это уже не в рамках тестового задания))
        raise Exception("Самосвал уже загружен!")
    TripTruck.objects.create(
        truck=truck,
        extraction_point=extraction_point,
        weight_tons=weight_tons,
        upload_datetime=timezone.now(),
    )


def unload_mineral_to_point(
    truck: Truck,
    unload_point: tuple,
) -> Union[WarehouseMoveMineralEvent, OutsideWarehouseMoveMineralEvent]:
    """Выгрузка руды из самосвала на точку
    Если точка оказывается вне склада выгрузка
    фиксируется в таблицу с промахами
    """
    warehouse = get_warehouse_by_geo_point(unload_point)
    trip = get_truck_current_trip(truck)
    if not trip:
        raise Exception("Самосвал пуст")
    # update trip
    trip.complite = True
    trip.unload_datetime = timezone.now()
    trip.unload_point = Point(*unload_point)
    if warehouse:
        trip.warehouse = warehouse
        unload_mineral_to_warehouse(
            warehouse=warehouse,
            extraction_point=trip.extraction_point,
            weight_tons=trip.weight_tons,
            trip_truck=trip,
        )
    else:
        unload_mineral_to_outside_warehouse(
            extraction_point=trip.extraction_point,
            weight_tons=trip.weight_tons,
            trip_truck=trip,
        )
    trip.save()


def get_truck_current_trip(truck: Truck) -> Union[TripTruck, bool]:
    """Получение текущего трека у самосвала"""
    current = TripTruck.objects.filter(truck__id=truck.id, complite=False)
    if current:
        return current[0]
    return False


def get_not_complited_trips():
    """Получение списка неоконченных треков"""
    return TripTruck.objects.prefetch_related("truck", "truck__model").filter(
        complite=False
    )
