"""Day 12: tenacity로 rate-limit 재시도 데모."""

from __future__ import annotations

import time

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from ai_study.logging import logger


class Fake429(Exception):
    pass


counter = {"n": 0}


@retry(
    retry=retry_if_exception_type(Fake429),
    wait=wait_random_exponential(min=1, max=30),
    stop=stop_after_attempt(5),
    reraise=True,
)
def flaky_call() -> str:
    counter["n"] += 1
    if counter["n"] < 4:
        logger.warning(f"simulated 429 (attempt {counter['n']})")
        raise Fake429("rate limit")
    return f"OK after {counter['n']} attempts"


if __name__ == "__main__":
    t0 = time.time()
    print(flaky_call())
    print(f"elapsed: {time.time() - t0:.1f}s")
