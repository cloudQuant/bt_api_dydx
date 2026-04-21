from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import nested_balance_handler as _dydx_balance_handler
from bt_api_dydx.exchange_data.dydx_exchange_data import DydxExchangeDataSwap
from bt_api_dydx.feeds.live_dydx.spot import DydxRequestDataSpot
from bt_api_base.registry import ExchangeRegistry


def _dydx_subscribe_handler(
    data_queue: Any,
    exchange_params: Any,
    topics: Any,
    bt_api: Any,
    exchange_data_cls: Any,
) -> None:
    topic_list = [i["topic"] for i in topics]

    if "ticker" in topic_list or "depth" in topic_list or "trades" in topic_list:
        bt_api.log("Market data subscription requested but WebSocket not implemented yet")

    if "account" in topic_list or "orders" in topic_list or "positions" in topic_list:
        bt_api.log("Account data subscription requested but WebSocket not implemented yet")

    bt_api.log("dYdX integration registered. REST API available.")


def _dydx_swap_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any
) -> None:
    _dydx_subscribe_handler(
        data_queue,
        exchange_params,
        topics,
        bt_api,
        DydxExchangeDataSwap,
    )


def _dydx_spot_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any
) -> None:
    _dydx_subscribe_handler(
        data_queue,
        exchange_params,
        topics,
        bt_api,
        DydxExchangeDataSwap,
    )


def register_dydx(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("DYDX___SWAP", DydxRequestDataSpot)
    registry.register_exchange_data("DYDX___SWAP", DydxExchangeDataSwap)
    registry.register_balance_handler("DYDX___SWAP", _dydx_balance_handler)
    registry.register_stream("DYDX___SWAP", "subscribe", _dydx_swap_subscribe_handler)

    registry.register_feed("DYDX___SPOT", DydxRequestDataSpot)
    registry.register_exchange_data("DYDX___SPOT", DydxExchangeDataSwap)
    registry.register_balance_handler("DYDX___SPOT", _dydx_balance_handler)
    registry.register_stream("DYDX___SPOT", "subscribe", _dydx_spot_subscribe_handler)
