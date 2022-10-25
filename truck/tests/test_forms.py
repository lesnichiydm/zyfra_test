from django.core.management import call_command
import pytest

from truck.forms import TruckListFormSet


def test_tuck_list_form():
    form = TruckListFormSet(
        data={
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-0-truck_pk": "1",
            "form-0-unload_point": "10 10",
            "form-1-truck_pk": "2",
            "form-1-unload_point": "1.11 2.33",
        }
    )
    assert form.is_valid()
    assert form.cleaned_data[0]["unload_point"] == (10.0, 10.0)
    assert form.cleaned_data[1]["unload_point"] == (1.11, 2.33)


@pytest.mark.xxx
def test_form_view(db, client):
    call_command("loaddata", "fixtures/all_fixtures.json")
    cli = client.post(
        "/",
        data={
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-0-truck_pk": "1",
            "form-0-unload_point": "30 10",
            "form-1-truck_pk": "2",
            "form-1-unload_point": "1.11 2.33",
            # "form-1-truck_pk": '3',
            # "form-1-unload_point": "2.11 2.33",
        },
    )
    assert cli.status_code == 302
    cli2 = client.get(cli.url)
    assert cli2.status_code == 200
