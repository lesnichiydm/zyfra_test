from django.contrib.gis.db.models import Q
from django.contrib.gis.geos import Point

from warehouse.models import Warehouse


def check_point_in_warehouse(warehouse, point):
    if isinstance(point, tuple):
        point = Point(*point)
    return warehouse.area.contains(point) or warehouse.area.touches(point)


def get_warehouse_by_geo_point(point):
    # __import__('pudb').set_trace()
    if isinstance(point, tuple):
        point = Point(*point)
    wh = Warehouse.objects.filter(
        Q(area__intersects=point) | Q(area__contains=point)
    )
    if wh:
        return wh[0]
    return False
