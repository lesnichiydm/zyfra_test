import pytest

from extraction_point.services import add_extraction_point, calc_mineral_info


def test_calc_mineral_info(db):
    ex_point = add_extraction_point(
        "P_1",
        percent_si_o_2=25,
        percent_fe=50,
    )

    info = calc_mineral_info(ex_point, 1000)
    assert info.si_o_2_tons == 250
    assert info.fe_tons == 500
    assert info.other_mineral_tons == 250
    assert info.si_o_2_percent == 25
    assert info.fe_percent == 50

    info2 = calc_mineral_info(ex_point, 2000)
    info += info2
    assert info.si_o_2_tons == 750
    assert info.fe_tons == 1500
