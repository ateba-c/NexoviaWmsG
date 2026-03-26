from rest_framework import serializers

from .models import InventoryMovement, InventoryPosition


class InventoryPositionSerializer(serializers.ModelSerializer):
    quantity_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = InventoryPosition
        fields = "__all__"


class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = "__all__"

