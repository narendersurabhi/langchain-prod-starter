# LangChain Production Starter

Production-ready LangChain + FastAPI starter with testable chains, RAG, and an agent demo.

## Architecture

```
+-------------+        +---------------------+       +----------------------+
|  FastAPI    |  --->  |  Chains (LCEL)      |  ---> |  LLM Provider        |
|  /chat      |        |  chat / rag / agent |       |  Fake / OpenAI / etc |
+------+------+        +---------+-----------+       +----------------------+
       |                         |
       |                         v
       |                 +---------------+
       |                 | Vector Store  |
       |                 | FAISS + docs  |
       |                 +---------------+
       v
+--------------+
| Observability|
| logs/metrics |
| traces       |
+--------------+
```

## Quickstart (Local)

```bash
cp .env.example .env
make setup
make run
```

Open `http://localhost:8000/docs` for the OpenAPI UI.

## Docker

```bash
docker build -t langchain-prod-starter .
docker run --rm -p 8000:8000 --env-file .env langchain-prod-starter
```

## Switching Providers

- Default is `LLM_PROVIDER=fake` for deterministic, offline runs.
- To use OpenAI:
  ```bash
  export LLM_PROVIDER=openai
  export OPENAI_API_KEY=sk-...
  ```
- To use Anthropic:
  ```bash
  export LLM_PROVIDER=anthropic
  export ANTHROPIC_API_KEY=...
  ```
- To use Ollama:
  ```bash
  export LLM_PROVIDER=ollama
  export OLLAMA_BASE_URL=http://localhost:11434
  ```

If provider credentials are missing, endpoints return a helpful error message and the app continues running.

## Endpoints

- `POST /chat` – LCEL chain (prompt → model → output parser)
- `POST /rag` – RAG with citations over local sample docs
- `POST /agent` – tool-using agent demo
- `GET /healthz` – liveness
- `GET /readyz` – readiness (includes vector store)
- `GET /metrics` – Prometheus

## Environment Variables

| Name | Description | Default |
| ---- | ----------- | ------- |
| `ENV` | `dev`/`prod`/`test` | `dev` |
| `LOG_LEVEL` | log level | `info` |
| `SERVICE_NAME` | service name | `lc_app` |
| `ENABLE_TRACING` | enable OpenTelemetry | `false` |
| `LLM_PROVIDER` | `fake`/`openai`/`anthropic`/`ollama` | `fake` |
| `OPENAI_API_KEY` | OpenAI key | empty |
| `ANTHROPIC_API_KEY` | Anthropic key | empty |
| `OLLAMA_BASE_URL` | Ollama base URL | empty |
| `RAG_TOP_K` | docs to retrieve | `4` |
| `VECTOR_STORE_PATH` | FAISS path | `.cache/vector_store` |
| `SAMPLE_DOCS_PATH` | sample docs path | `data/sample_docs` |

## Testing

```bash
make test
```

## Troubleshooting

- **RAG returns degraded readiness**: ensure `data/sample_docs` exists or delete `.cache/vector_store` to rebuild.
- **Provider errors**: ensure the provider env vars are set or revert to `LLM_PROVIDER=fake`.
- **Tracing export failures**: disable tracing with `ENABLE_TRACING=false` if no OTLP collector is available.

## Development Commands

```bash
make format
make lint
make type
make test
```
