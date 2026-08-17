import pytest

import fetcher


def _response(status_code=200, text="", from_cache=False):
    """Helper function to create a mock response object."""
    return type(
        "Response",
        (),
        {"status_code": status_code, "text": text, "from_cache": from_cache},
    )()


def test_fetch_rate_limit_uses_configured_delay(mocker):
    mocker.patch("fetcher.session.cache.contains", side_effect=[False])
    mocker.patch("fetcher.time.monotonic", side_effect=[0, 1])
    mocker.patch("fetcher.time.sleep")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(),
    )

    mocker.patch.object(fetcher, "_last_request_ts", 1.0)

    random_mock = mocker.patch("fetcher.random.uniform", return_value=3)
    mocker.patch("config.REQUEST_MIN_DELAY_SECONDS", 100)
    mocker.patch("config.REQUEST_MAX_DELAY_SECONDS", 200)

    fetcher.fetch("https://example.test/item/1")
    random_mock.assert_called_once_with(100, 200)


def test_fetch_rate_limit_skipped_on_first_request(mocker):
    mocker.patch("fetcher.session.cache.contains", side_effect=[False, False])
    mocker.patch("fetcher.time.monotonic", side_effect=[100, 101])
    mocker.patch("fetcher.random.uniform", side_effect=[1, 3])
    sleep_mock = mocker.patch("fetcher.time.sleep")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(),
    )

    mocker.patch.object(fetcher, "_last_request_ts", 0.0)

    # last_request = 0, time = 100, elapsed = 100, delay = 1, wait = -99
    fetcher.fetch("https://example.test/item/1")
    sleep_mock.assert_not_called()


def test_fetch_rate_limit_reduced_by_elapsed_time(mocker):
    mocker.patch("fetcher.session.cache.contains", side_effect=[False, False])
    mocker.patch("fetcher.time.monotonic", side_effect=[0, 1, 2, 3])
    mocker.patch("fetcher.random.uniform", side_effect=[1, 3])
    sleep_mock = mocker.patch("fetcher.time.sleep")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(),
    )

    mocker.patch.object(fetcher, "_last_request_ts", 0.0)

    # last_request = 0, time = 0, elapsed = 0, delay = 1, wait = 1
    fetcher.fetch("https://example.test/item/1")
    assert sleep_mock.call_args[0][0] == 1

    # last_request = 1, time = 2, elapsed = 1, delay = 3, wait = 2
    fetcher.fetch("https://example.test/item/2")
    assert sleep_mock.call_args[0][0] == 2
    assert sleep_mock.call_count == 2


def test_fetch_rate_limit_skipped_when_elapsed_time_exceeds_delay(mocker):
    mocker.patch("fetcher.session.cache.contains", side_effect=[False, False])
    mocker.patch("fetcher.time.monotonic", side_effect=[0, 1, 40, 50])
    mocker.patch("fetcher.random.uniform", side_effect=[1, 3])
    sleep_mock = mocker.patch("fetcher.time.sleep")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(),
    )

    mocker.patch.object(fetcher, "_last_request_ts", 0.0)

    # last_request = 0, time = 0, elapsed = 0, delay = 1, wait = 1
    fetcher.fetch("https://example.test/item/1")
    assert sleep_mock.call_args[0][0] == 1

    # last_request = 1, time = 40, elapsed = 39, delay = 3, wait = -36
    fetcher.fetch("https://example.test/item/2")
    assert sleep_mock.call_count == 1


def test_fetch_rate_limit_applied_to_uncached_requests(mocker):
    mocker.patch("fetcher.session.cache.contains", return_value=False)
    rate_limit_mock = mocker.patch("fetcher._rate_limit")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(),
    )

    fetcher.fetch("https://example.test/item/1")
    rate_limit_mock.assert_called_once()


def test_fetch_rate_limit_not_applied_to_cached_requests(mocker):
    mocker.patch("fetcher.session.cache.contains", return_value=True)
    rate_limit_mock = mocker.patch("fetcher._rate_limit")

    mocker.patch(
        "fetcher.session.get",
        return_value=_response(from_cache=True),
    )

    fetcher.fetch("https://example.test/item/1")
    rate_limit_mock.assert_not_called()


def test_fetch_returns_html_for_successful_response(mocker):
    mocker.patch("fetcher.session.cache.contains", return_value=True)
    mocker.patch(
        "fetcher.session.get",
        return_value=_response(text="<html>data</html>", from_cache=True),
    )

    result = fetcher.fetch("https://example.test/item/1")
    assert result == ("<html>data</html>", True)


def test_fetch_returns_invalid_for_redirect(mocker):
    mocker.patch("fetcher.session.cache.contains", return_value=True)
    mocker.patch(
        "fetcher.session.get",
        return_value=_response(status_code=302, from_cache=True),
    )

    result = fetcher.fetch("https://example.test/item/1")
    assert result == (None, False)


@pytest.mark.parametrize("status_code", [400, 403, 404, 429, 500, 503])
def test_fetch_raises_for_unexpected_status(mocker, status_code):
    mocker.patch("fetcher.session.cache.contains", return_value=True)
    mocker.patch(
        "fetcher.session.get",
        return_value=_response(status_code=status_code, from_cache=True),
    )

    with pytest.raises(
        RuntimeError,
        match=f"Unexpected status code {status_code} for URL: https://example.test/item/1",
    ):
        fetcher.fetch("https://example.test/item/1")
