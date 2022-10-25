from typing import Union
from django.db.models import Sum

from extraction_point.models import ExtractionPoint
from extraction_point.services import MineralInfo, calc_mineral_info
from truck.models import Truck
from warehouse.models import (
    OutsideWarehouseMoveMineralEvent,
    Warehouse,
    WarehouseMoveMineralEvent,
)


def add_warehouse(name, area):
    """Создание склада"""
    return Warehouse.objects.create(name=name, area=area)


def unload_mineral_to_warehouse(
    extraction_point: ExtractionPoint,
    weight_tons: int,
    warehouse: Warehouse,
    trip_truck: Union[Truck, None] = None,
) -> WarehouseMoveMineralEvent:
    """Выгрузка руды на склад"""
    mineral_info = calc_mineral_info(extraction_point, weight_tons)
    return WarehouseMoveMineralEvent.objects.create(
        warehouse=warehouse,
        extraction_point=extraction_point,
        total_tons=weight_tons,
        trip_truck=trip_truck,
        si_o_2_tons=mineral_info.si_o_2_tons,
        fe_tons=mineral_info.fe_tons,
    )


def unload_mineral_to_outside_warehouse(
    extraction_point: ExtractionPoint,
    weight_tons: int,
    trip_truck: Union[Truck, None] = None,
) -> OutsideWarehouseMoveMineralEvent:
    """Выгрузка руды мимо склада"""
    mineral_info = calc_mineral_info(extraction_point, weight_tons)
    return OutsideWarehouseMoveMineralEvent.objects.create(
        extraction_point=extraction_point,
        total_tons=weight_tons,
        trip_truck=trip_truck,
        si_o_2_tons=mineral_info.si_o_2_tons,
        fe_tons=mineral_info.fe_tons,
    )


def get_warehouse_mineral_info(warehouse: Warehouse) -> MineralInfo:
    """Получение сводных данных по содержанию руды на складе"""
    info = WarehouseMoveMineralEvent.objects.filter(
        warehouse=warehouse
    ).aggregate(Sum("si_o_2_tons"), Sum("fe_tons"), Sum("total_tons"))
    return MineralInfo(
        si_o_2_tons=info["si_o_2_tons__sum"],
        fe_tons=info["fe_tons__sum"],
        total_tons=info["total_tons__sum"],
    )
