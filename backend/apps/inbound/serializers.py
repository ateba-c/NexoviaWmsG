from rest_framework import serializers

from .models import InboundLine, InboundOrder, ReceiveEvent


class InboundOrderSerializer(serializers.ModelSerializer):
    line_count = serializers.SerializerMethodField()

    class Meta:
        model = InboundOrder
        fields = "__all__"

    def get_line_count(self, obj: InboundOrder) -> int:
        return obj.lines.count()


class InboundLineSerializer(serializers.ModelSerializer):
    item_sku = serializers.CharField(source="item.sku", read_only=True)
    order_number = serializers.CharField(source="inbound_order.order_number", read_only=True)
    supplier_name = serializers.CharField(source="inbound_order.supplier_name", read_only=True)
    qty_remaining = serializers.SerializerMethodField()

    class Meta:
        model = InboundLine
        fields = "__all__"

    def get_qty_remaining(self, obj: InboundLine) -> int:
        return max(obj.qty_expected - obj.qty_received, 0)


class ReceiveEventSerializer(serializers.ModelSerializer):
    location_code = serializers.CharField(source="location.code", read_only=True)
    item_sku = serializers.CharField(source="inbound_line.item.sku", read_only=True)

    class Meta:
        model = ReceiveEvent
        fields = "__all__"


class ReceiveLineSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    location = serializers.UUIDField()
    lot_number = serializers.CharField(required=False, allow_blank=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)
