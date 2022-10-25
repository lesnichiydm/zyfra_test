from rest_framework import serializers

from .models import Warehouse


class WarehouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["url", "name", "area"]
