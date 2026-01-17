import httpx


async def test_health_and_ready(app):
    transport = httpx.ASGITransport(app=app, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/healthz")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        ready = await client.get("/readyz")
        assert ready.status_code == 200
        assert ready.json()["vector_store"] == "ready"
