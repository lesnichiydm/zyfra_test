import pytest

from extraction_point.services import add_extraction_point
from truck.services.base import unload_mineral_to_point
from warehouse.models import Warehouse
from warehouse.services.base import (add_warehouse, get_warehouse_mineral_info,
                                     unload_mineral_to_warehouse)
from warehouse.services.geo import (check_point_in_warehouse,
                                    get_warehouse_by_geo_point)


def test_warehouse_unload_area(db):
    # base poly
    wh1 = add_warehouse(
        name="test1", area="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
    )
    assert not check_point_in_warehouse(wh1, (100, 100))
    assert check_point_in_warehouse(wh1, (30, 10))
    # square
    wh2 = add_warehouse(
        name="test2", area="POLYGON ((0 0, 0 10, 10 10, 10 0, 0 0))"
    )
    assert check_point_in_warehouse(wh2, (0, 0))
    assert check_point_in_warehouse(wh2, (1, 1))
    assert check_point_in_warehouse(wh2, (9, 10))
    assert not check_point_in_warehouse(wh2, (10.001, 10))
    # triangle
    wh3 = Warehouse.objects.create(
        name="wh3", area="POLYGON ((0 0, 0 4, 4 0, 0 0))"
    )
    assert check_point_in_warehouse(wh3, (2, 2))


def test_get_warehouse_by_geo_poin(db):
    # base poly
    wh1 = add_warehouse(
        name="test1", area="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
    )
    assert wh1 == get_warehouse_by_geo_point((30, 10))
    wh1.delete()
    # square
    wh2 = add_warehouse(
        name="test2", area="POLYGON ((0 0, 0 10, 10 10, 10 0, 0 0))"
    )
    assert wh2 == get_warehouse_by_geo_point((0, 0))
    assert wh2 == get_warehouse_by_geo_point((1, 1))
    assert wh2 == get_warehouse_by_geo_point((9, 10))
    assert not get_warehouse_by_geo_point((19, 10))
    wh2.delete()
    # triangle
    wh3 = Warehouse.objects.create(
        name="wh3", area="POLYGON ((0 0, 0 4, 4 0, 0 0))"
    )
    assert wh3 == get_warehouse_by_geo_point((2, 2))
    assert not get_warehouse_by_geo_point((2.0001, 2))


def test_unload_mineral_to_warehouse(db):
    warehouse = add_warehouse(
        name="Test",
        area="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
    )
    unload_mineral_to_warehouse(
        add_extraction_point(
            "Fake_for_initial",
            percent_si_o_2=25,
            percent_fe=50,
        ),
        weight_tons=2000,
        warehouse=warehouse,
    )
    info = get_warehouse_mineral_info(warehouse)
    assert info.si_o_2_tons == 500 and info.fe_tons == 1000
    assert info.total_tons == 2000

    unload_mineral_to_warehouse(
        add_extraction_point(
            "Fake2_for_initial",
            percent_si_o_2=20,
            percent_fe=40,
        ),
        weight_tons=1000,
        warehouse=warehouse,
    )
    info2 = get_warehouse_mineral_info(warehouse)
    assert info2.total_tons == 3000
    assert info2.si_o_2_tons == 700 and info2.fe_tons == 1400
