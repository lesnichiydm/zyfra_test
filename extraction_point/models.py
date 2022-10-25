from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ExtractionPoint(models.Model):
    """Точки загрузки(забора) руды"""

    name = models.CharField(
        "Название точки загрузки",
        max_length=255,
    )
    percent_si_o_2 = models.FloatField(
        verbose_name="Процентное содержание диоксида кремния",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    percent_fe = models.FloatField(
        verbose_name="Процентное содержание железа",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Точки загрузки руды"
