from rest_framework import serializers

from .models import KPIReport, MetricSnapshot


class MetricSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricSnapshot
        fields = "__all__"


class KPIReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIReport
        fields = "__all__"
