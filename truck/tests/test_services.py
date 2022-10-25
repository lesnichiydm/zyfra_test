from typing import Callable

import pytest

from extraction_point.services import add_extraction_point
from truck.services.base import (
    add_mineral_to_truck,
    add_truck,
    add_truck_model_if_not_exist,
    add_truck_with_model,
    calc_truck_capacity_owerload_percent,
    get_not_complited_trips,
)


def test_add_new_truck_model(db):
    t1 = add_truck_model_if_not_exist(name="Model_1", capacity=120)
    t2 = add_truck_model_if_not_exist(name="Model_1", capacity=160)
    assert t1.capacity == 120 and t2.capacity == 160


def test_add_truck(db):
    tm = add_truck_model_if_not_exist(name="Model_1", capacity=120)
    truck = add_truck(side_number="101", model=tm)
    assert truck.capacity == 120


def test_add_truck_whith_model(db):
    truck = add_truck_with_model(
        side_number="123x",
        model_name="Model_3",
        capacity=140,
    )
    assert truck.capacity == 140


def test_calc_owerload(db):
    truck = add_truck_with_model(
        side_number="123x",
        model_name="Model_3",
        capacity=100,
    )
    assert calc_truck_capacity_owerload_percent(truck, 150) == 50
    assert calc_truck_capacity_owerload_percent(truck, 50) == 0


def test_get_full_trucks(db):
    truck1 = add_truck_with_model("101", "БЕЛАЗ", 120)
    truck2 = add_truck_with_model("K103", "Komatsu", 110)
    truck3 = add_truck_with_model("103", "БЕЛАЗ", 120)
    ex_point1 = add_extraction_point("P_1", percent_si_o_2=20, percent_fe=30)
    add_mineral_to_truck(
        truck=truck1,
        extraction_point=ex_point1,
        weight_tons=100,
    )
    add_mineral_to_truck(
        truck=truck2,
        extraction_point=ex_point1,
        weight_tons=100,
    )

    assert len(get_not_complited_trips()) == 2
