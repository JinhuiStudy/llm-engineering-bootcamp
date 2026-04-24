"""Rate-limit/일시 에러 자동 재시도 wrapper."""

from __future__ import annotations

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

# provider별 rate limit 클래스 가져오기 (optional import로 안전)
try:  # pragma: no cover
    from openai import APIError as OpenAIAPIError
    from openai import RateLimitError as OpenAIRateLimit
except Exception:  # noqa: BLE001
    OpenAIAPIError = Exception  # type: ignore
    OpenAIRateLimit = Exception  # type: ignore

try:  # pragma: no cover
    from anthropic import APIError as AnthropicAPIError
    from anthropic import RateLimitError as AnthropicRateLimit
except Exception:  # noqa: BLE001
    AnthropicAPIError = Exception  # type: ignore
    AnthropicRateLimit = Exception  # type: ignore

_RETRYABLE = (
    OpenAIRateLimit,
    OpenAIAPIError,
    AnthropicRateLimit,
    AnthropicAPIError,
    TimeoutError,
    ConnectionError,
)


def with_retry(fn):
    """함수에 exponential backoff + jitter 씌우기.

    사용:
        @with_retry
        def call_llm(...): ...
    """
    return retry(
        reraise=True,
        retry=retry_if_exception_type(_RETRYABLE),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(5),
    )(fn)
