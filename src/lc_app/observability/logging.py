from __future__ import annotations

import logging
from typing import Any

import structlog


def setup_logging(log_level: str) -> None:
    logging.basicConfig(format="%(message)s", level=log_level.upper())

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level.upper()),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.stdlib.BoundLogger:
    return structlog.get_logger()


def log_request(logger: structlog.stdlib.BoundLogger, **kwargs: Any) -> None:
    logger.info("request", **kwargs)
