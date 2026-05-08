"""Tests for retry handler behavior."""

from src.core.retry_handler import RetryHandler


def test_retry_schedule_respects_max_delay():
    handler = RetryHandler(
        max_attempts=4,
        initial_delay=1,
        max_delay=3,
        backoff_multiplier=2,
    )

    assert handler.get_retry_schedule() == [1, 2, 3, 3]


def test_execute_retries_until_success():
    state = {"attempts": 0}
    handler = RetryHandler(
        max_attempts=3,
        initial_delay=0,
        max_delay=0,
        backoff_multiplier=2,
    )

    def flaky():
        state["attempts"] += 1
        if state["attempts"] < 3:
            raise RuntimeError("temporary")
        return "ok"

    result = handler.execute(flaky)

    assert result == "ok"
    assert state["attempts"] == 3
