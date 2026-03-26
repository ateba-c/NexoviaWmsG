from rest_framework import serializers

from .models import LPN


class LPNSerializer(serializers.ModelSerializer):
    class Meta:
        model = LPN
        fields = "__all__"

