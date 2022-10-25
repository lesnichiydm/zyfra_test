from django.contrib.gis.db import models


class Warehouse(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
    )
    area = models.PolygonField(
        verbose_name="Область склада",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class WarehouseMoveMineralEventAbs(models.Model):
    """
    Общая модель событий загрузки-выгрузки со склада
    """

    datetime = models.DateTimeField(
        "Время события",
        auto_now_add=True,
    )
    extraction_point = models.ForeignKey(
        "extraction_point.ExtractionPoint",
        verbose_name="Откуда привезли",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    trip_truck = models.ForeignKey(
        "truck.TripTruck",
        verbose_name="Грузовик совершивший действие",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    total_tons = models.FloatField("Масса всей выгрузки")
    si_o_2_tons = models.FloatField("Масса диоксида кремния")
    fe_tons = models.FloatField("Масса железа")

    class Meta:
        abstract = True


class WarehouseMoveMineralEvent(WarehouseMoveMineralEventAbs):
    """
    Модель событий загрузки-выгрузки со склада
    """

    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name="Склад",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Движение по складу"


class OutsideWarehouseMoveMineralEvent(WarehouseMoveMineralEventAbs):
    """
    Модель событий выгрузки мимо склада. Логичнее вынести
    в отдельную сущность так как вероятно в основных процессах
    она учавствовать не будет и данные записи будут создавать
    неудобства в работе
    """

    class Meta:
        verbose_name = "Отвалы промахи вокруг склада"
