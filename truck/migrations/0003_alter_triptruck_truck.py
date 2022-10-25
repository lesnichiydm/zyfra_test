# Generated by Django 4.1.2 on 2022-10-24 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("truck", "0002_triptruck"),
    ]

    operations = [
        migrations.AlterField(
            model_name="triptruck",
            name="truck",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trip",
                to="truck.truck",
                verbose_name="Самосвал",
            ),
        ),
    ]
