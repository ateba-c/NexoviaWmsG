from rest_framework import serializers

from .models import Manifest, Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"


class ManifestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manifest
        fields = "__all__"


class ShipmentMarkShippedSerializer(serializers.Serializer):
    tracking_number = serializers.CharField(required=False, allow_blank=True)
