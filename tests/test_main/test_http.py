from ssg import app


async def test_get_index():
    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200
    text = await response.get_data()
    assert b"<form" in text


async def test_create_game_and_redirect():
    test_client = app.test_client()

    form = {"game-style": "local", "difficulty": "1", "color": "red"}

    response = await test_client.post("/", form=form)
    assert response.status_code == 302

    location = response.headers["Location"]
    assert location.startswith("/")

    # Follow redirect to game page
    game_page = await test_client.get(location)
    html = await game_page.get_data()
    assert b"New Game" in html


async def test_game_route_redirects_on_invalid_code():
    test_client = app.test_client()
    response = await test_client.get("/XXXX")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
