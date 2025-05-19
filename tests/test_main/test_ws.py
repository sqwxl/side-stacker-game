import json


from ssg import app


async def test_join_and_receive_broadcast():
    test_client = app.test_client()

    form = {"game-style": "local", "difficulty": "1", "color": "red"}

    post = await test_client.post("/", form=form)
    game_code = post.headers["Location"]

    async with test_client.websocket(f"{game_code}/ws") as ws:
        # Valid move message from player
        ws_message = {"action": {"name": "play", "payload": {"col": 0, "row": 0}}}

        await ws.send(json.dumps(ws_message))

        # Receive updated board HTML
        message: str = await ws.receive()
        assert '<div id="board"' in message
