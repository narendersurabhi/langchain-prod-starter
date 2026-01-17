import httpx


async def test_agent_endpoint(app):
    transport = httpx.ASGITransport(app=app, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/agent", json={"task": "What time is it?"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["tool_calls"][0]["tool"] == "current_time"
        assert payload["result"].endswith("Z")
