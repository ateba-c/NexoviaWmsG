from rest_framework import serializers

from .models import Container, OrderLine, OutboundOrder, PickTask, Wave, WaveOrder


class OutboundOrderSerializer(serializers.ModelSerializer):
    line_count = serializers.SerializerMethodField()

    class Meta:
        model = OutboundOrder
        fields = "__all__"

    def get_line_count(self, obj: OutboundOrder) -> int:
        return obj.lines.count()


class OrderLineSerializer(serializers.ModelSerializer):
    item_sku = serializers.CharField(source="item.sku", read_only=True)
    order_number = serializers.CharField(source="outbound_order.order_number", read_only=True)

    class Meta:
        model = OrderLine
        fields = "__all__"


class WaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wave
        fields = "__all__"


class WaveOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaveOrder
        fields = "__all__"


class PickTaskSerializer(serializers.ModelSerializer):
    location_code = serializers.CharField(source="inventory_position.location.code", read_only=True)
    item_sku = serializers.CharField(source="order_line.item.sku", read_only=True)
    order_number = serializers.CharField(source="order_line.outbound_order.order_number", read_only=True)
    quantity_remaining = serializers.SerializerMethodField()

    class Meta:
        model = PickTask
        fields = "__all__"

    def get_quantity_remaining(self, obj: PickTask) -> int:
        return max(obj.quantity_to_pick - obj.quantity_picked, 0)


class PickTaskConfirmSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"
