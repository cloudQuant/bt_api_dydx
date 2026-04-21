import pytest
from bt_api_dydx.feeds.live_dydx.request_base import DydxRequestData
def test_dydx_accepts_public_private_key_aliases() -> None:
    request_data = DydxRequestData(
        None,
        public_key="public-key",
        private_key="secret-key",
    )

    assert request_data.api_key == "public-key"
    assert request_data.private_key == "secret-key"
