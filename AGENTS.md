# Agent Change Log

This file tracks changes made by automated agents in this repository.

## 2025-09-03
- Added core application scaffolding (FastAPI app, middleware, observability, settings, errors, utils).
- Implemented fake LLM + deterministic embeddings and LLM factory.
- Added LCEL chat chain, RAG chain + vector store ingestion, and tool-using agent chain.
- Added API routes for chat, rag, agent, health, readiness, and metrics with tracing hooks.
- Created sample docs for RAG and vector store ingestion helpers.
- Added test suite for health, chat, rag, agent, and ingestion.
- Added project tooling (pyproject, Makefile, pre-commit), CI workflow, Dockerfile, docker-compose.
- Added repository docs and governance files (README, CONTRIBUTING, SECURITY, CODEOWNERS, issue/PR templates).
- Updated build configuration to explicitly include the src package for editable installs.
