# Generated by Django 4.1.2 on 2022-10-24 11:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExtractionPoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Название точки загрузки"
                    ),
                ),
                (
                    "percent_si_o_2",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(100.0),
                        ],
                        verbose_name="Процентное содержание диоксида кремния",
                    ),
                ),
                (
                    "percent_fe",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(100.0),
                        ],
                        verbose_name="Процентное содержание железа",
                    ),
                ),
            ],
        ),
    ]
