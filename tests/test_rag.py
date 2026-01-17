import httpx


async def test_rag_endpoint(app):
    transport = httpx.ASGITransport(app=app, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/rag", json={"question": "When does coverage start?"})
        assert response.status_code == 200
        payload = response.json()
        assert "day one" in payload["answer"].lower()
        assert payload["citations"]
