from extraction_point.services import calc_mineral_info
from truck.models import Truck
from truck.services.base import get_truck_current_trip
from warehouse.services.base import get_warehouse_mineral_info
from warehouse.services.geo import get_warehouse_by_geo_point


def calc_warehouses_info_after_upload_mineral(trucks_unload):
    """
    Принимаем словарь с ключем truck_id и значением
    точка сброса (x, y)
    """
    # если словарь прилетел из джаго-сесии приводим в базовый вид
    trucks_unload = {int(k): tuple(v) for k, v in trucks_unload.items()}

    trucks = Truck.objects.filter(pk__in=trucks_unload.keys())
    warehouse_tmp = {}
    for i in trucks:
        wh = get_warehouse_by_geo_point(trucks_unload[i.pk])
        # Промах мимо цели
        if not wh:
            continue
        # Если это новый склад
        if wh.pk not in warehouse_tmp:
            condition = get_warehouse_mineral_info(wh)
            warehouse_tmp[wh.pk] = {
                "obj": wh,
                "weight_tons_pre_upload": condition.total_tons,
                "condition": condition,
            }
        # Узнаем что сгружаем
        trip_truck = get_truck_current_trip(i)
        mineral_info = calc_mineral_info(
            trip_truck.extraction_point,
            trip_truck.weight_tons,
        )
        # Добавляем это к складу
        warehouse_tmp[wh.pk]["condition"] += mineral_info
    return [
        {
            "name": i["obj"].name,
            "weight_tons_pre_upload": i["weight_tons_pre_upload"],
            "weight_tons": i["condition"].total_tons,
            "minerals_info": i["condition"].description,
        }
        for i in warehouse_tmp.values()
    ]
