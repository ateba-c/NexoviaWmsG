from rest_framework import serializers

from .models import CountResult, CountTask, CountVariance


class CountTaskSerializer(serializers.ModelSerializer):
    location_code = serializers.CharField(source="location.code", read_only=True)
    result_count = serializers.SerializerMethodField()
    latest_item_id = serializers.SerializerMethodField()
    latest_item_sku = serializers.SerializerMethodField()

    class Meta:
        model = CountTask
        fields = "__all__"

    def get_result_count(self, obj: CountTask) -> int:
        return obj.results.count()

    def _get_latest_result(self, obj: CountTask):
        return obj.results.select_related("item").order_by("-created_at").first()

    def get_latest_item_id(self, obj: CountTask):
        latest_result = self._get_latest_result(obj)
        return str(latest_result.item_id) if latest_result else ""

    def get_latest_item_sku(self, obj: CountTask) -> str:
        latest_result = self._get_latest_result(obj)
        return latest_result.item.sku if latest_result else ""


class CountResultSerializer(serializers.ModelSerializer):
    item_sku = serializers.CharField(source="item.sku", read_only=True)

    class Meta:
        model = CountResult
        fields = "__all__"


class CountVarianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountVariance
        fields = "__all__"


class ExecuteCountSerializer(serializers.Serializer):
    item = serializers.UUIDField()
    counted_quantity = serializers.IntegerField(min_value=0)
