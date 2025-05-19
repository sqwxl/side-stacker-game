from asyncio import Queue
from collections.abc import AsyncGenerator


class Broker:
    def __init__(self) -> None:
        self.connections: dict[int, Queue[str]] = {}

    async def publish(self, message: str, player_ids: list[int] | None = None) -> None:
        targets = player_ids if player_ids is not None else self.connections.keys()
        for player_id in targets:
            queue = self.connections.get(player_id)
            if queue:
                await queue.put(message)

    async def subscribe(self, player_id: int) -> AsyncGenerator[str, None]:
        queue: Queue[str] = Queue()
        self.connections[player_id] = queue
        try:
            while True:
                yield await queue.get()
        finally:
            self.connections.pop(player_id, None)


# Keep track of brokers on a per-game basis
class BrokerHub:
    def __init__(self) -> None:
        self._brokers: dict[str, Broker] = {}

    def get(self, code: str) -> Broker:
        if code not in self._brokers:
            self._brokers[code] = Broker()
        return self._brokers[code]
