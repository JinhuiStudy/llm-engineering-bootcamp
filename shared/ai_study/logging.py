"""loguru 기반 간단 로깅 설정.

import 시점에 한 번 설정. day별 프로젝트에서:
    from ai_study.logging import logger
    logger.info("...")
"""

from __future__ import annotations

import sys

from loguru import logger as _logger

from ai_study.config import settings

_logger.remove()
_logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <7}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:{line} - "
    "<level>{message}</level>",
    colorize=True,
)

logger = _logger

__all__ = ["logger"]
