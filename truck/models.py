from django.contrib.gis.db import models as gis_models
from django.db import models


class TruckModel(models.Model):
    """Модели грузовиков"""

    name = models.CharField("Модель грузовика", max_length=255)
    capacity = models.PositiveIntegerField("Грузоподьемность тонн")

    def __str__(self):
        return f"{self.name} - {self.capacity}т"

    class Meta:
        verbose_name = "Модель грузовика"
        verbose_name_plural = "Модели грузовиков"
        unique_together = ("name", "capacity")


class Truck(models.Model):
    """Грузовики"""

    side_number = models.CharField(
        "Бортовой номер", max_length=10, unique=True
    )
    model = models.ForeignKey(
        TruckModel,
        verbose_name="Модель",
        related_name="trucks",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.side_number} ({self.model})"

    @property
    def capacity(self):
        return self.model.capacity

    class Meta:
        verbose_name = "Самосвал"
        verbose_name_plural = "Самосвалы"


class TripTruck(gis_models.Model):
    """Поездки самосвала карьер-склад"""

    truck = gis_models.ForeignKey(
        Truck,
        verbose_name="Самосвал",
        on_delete=gis_models.CASCADE,
        related_name="trip",
    )
    complite = gis_models.BooleanField(
        verbose_name="Признак окончания поездки и опустошения кузова",
        default=False,
    )
    extraction_point = gis_models.ForeignKey(
        "extraction_point.ExtractionPoint",
        verbose_name="Точка загрузки",
        on_delete=gis_models.CASCADE,
        null=True,
        blank=True,
    )
    weight_tons = gis_models.FloatField(
        verbose_name="Сколько тон загружено",
        null=True,
        blank=True,
    )
    upload_datetime = gis_models.DateTimeField(
        verbose_name="Время погрузки",
        null=True,
        blank=True,
    )
    warehouse = gis_models.ForeignKey(
        "warehouse.Warehouse",
        verbose_name="Склад выгрузки",
        on_delete=gis_models.CASCADE,
        null=True,
        blank=True,
    )
    unload_point = gis_models.PointField(
        verbose_name="Координаты выгрузки",
        null=True,
        blank=True,
    )
    unload_datetime = gis_models.DateTimeField(
        verbose_name="Время выгрузки",
        null=True,
        blank=True,
    )
