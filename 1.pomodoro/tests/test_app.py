from app import create_app


def test_index_route_returns_200() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "ポモドーロタイマー" in html
    assert 'id="timer-ring"' in html
    assert 'id="start-button"' in html
    assert 'id="reset-button"' in html
    assert 'id="daily-progress"' in html


def test_health_route_returns_ok() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
