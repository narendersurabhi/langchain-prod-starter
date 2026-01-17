from __future__ import annotations

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "HTTP request count",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_ms",
    "HTTP request latency in ms",
    ["method", "path", "status"],
    buckets=(1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000),
)
