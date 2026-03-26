from __future__ import annotations

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class OperationsConsumer(AsyncJsonWebsocketConsumer):
    group_name = "operations"

    async def connect(self) -> None:
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def operations_event(self, event: dict) -> None:
        await self.send_json(event["payload"])

