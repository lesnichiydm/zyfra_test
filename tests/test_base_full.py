import pytest
from django.core.management import call_command

from extraction_point.services import add_extraction_point
from truck.services.base import (add_mineral_to_truck, add_truck_with_model,
                                 unload_mineral_to_point)
from warehouse.services.base import (add_warehouse, get_warehouse_mineral_info,
                                     unload_mineral_to_warehouse)


def test_full_case(db):
    truck1 = add_truck_with_model("101", "БЕЛАЗ", 120)
    truck2 = add_truck_with_model("K103", "Komatsu", 110)
    truck3 = add_truck_with_model("103", "БЕЛАЗ", 120)

    ex_point1 = add_extraction_point("P_1", percent_si_o_2=20, percent_fe=30)
    ex_point2 = add_extraction_point("P_2", percent_si_o_2=30, percent_fe=40)

    warehouse = add_warehouse(
        name="Test",
        area="POLYGON ((0 0, 0 10, 10 10, 10 0, 0 0))",
    )
    unload_mineral_to_warehouse(
        add_extraction_point(
            "Fake_for_initial",
            percent_si_o_2=10,
            percent_fe=10,
        ),
        weight_tons=100,
        warehouse=warehouse,
    )

    add_mineral_to_truck(
        truck=truck1,
        extraction_point=ex_point1,
        weight_tons=100,
    )
    add_mineral_to_truck(
        truck=truck2,
        extraction_point=ex_point1,
        weight_tons=200,
    )
    add_mineral_to_truck(
        truck=truck3,
        extraction_point=ex_point1,
        weight_tons=100,
    )

    unload_mineral_to_point(truck1, unload_point=(10, 1))
    assert get_warehouse_mineral_info(warehouse).total_tons == 200

    unload_mineral_to_point(truck2, unload_point=(10, 10))
    assert get_warehouse_mineral_info(warehouse).total_tons == 400
    # Загружаем мимо склада
    unload_mineral_to_point(truck3, unload_point=(11, 10))
    assert get_warehouse_mineral_info(warehouse).total_tons == 400


@pytest.mark.skip
def test_full_case_tz_for_fixtures(db):
    """
    Полный кейс из ТЗ для генерации фикстуры
    """
    truck1 = add_truck_with_model("101", "БЕЛАЗ", 120)
    truck2 = add_truck_with_model("102", "БЕЛАЗ", 120)
    truck3 = add_truck_with_model("K103", "Komatsu", 110)

    ex_point1 = add_extraction_point("P_1", percent_si_o_2=32, percent_fe=67)
    ex_point2 = add_extraction_point("P_2", percent_si_o_2=30, percent_fe=65)
    ex_point3 = add_extraction_point("P_1", percent_si_o_2=35, percent_fe=62)

    warehouse = add_warehouse(
        name="Test",
        area="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
    )
    unload_mineral_to_warehouse(
        add_extraction_point(
            "Fake_for_initial",
            percent_si_o_2=34,
            percent_fe=65,
        ),
        weight_tons=900,
        warehouse=warehouse,
    )

    add_mineral_to_truck(
        truck=truck1,
        extraction_point=ex_point1,
        weight_tons=100,
    )
    add_mineral_to_truck(
        truck=truck2,
        extraction_point=ex_point1,
        weight_tons=125,
    )
    add_mineral_to_truck(
        truck=truck3,
        extraction_point=ex_point1,
        weight_tons=120,
    )

    call_command(
        "dumpdata",
        ["warehouse", "truck", "extraction_point"],
        indent=4,
        output="fixtures/all_fixtures.json",
    )
