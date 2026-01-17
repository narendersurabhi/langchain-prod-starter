import httpx


async def test_chat_endpoint(app):
    transport = httpx.ASGITransport(app=app, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "Hello"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["response"].startswith("Fake response")
        assert payload["request_id"]
