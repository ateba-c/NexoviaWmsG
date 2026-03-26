from rest_framework import serializers

from .models import Disposition, ReturnLine, ReturnOrder


class ReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnOrder
        fields = "__all__"


class ReturnLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnLine
        fields = "__all__"


class DispositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disposition
        fields = "__all__"
