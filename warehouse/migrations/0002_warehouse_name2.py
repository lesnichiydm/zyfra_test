# Generated by Django 4.1.2 on 2022-10-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="warehouse",
            name="name2",
            field=models.CharField(
                default="", max_length=255, verbose_name="Название"
            ),
            preserve_default=False,
        ),
    ]