from __future__ import annotations

import datetime
import json
import time
from typing import Any

from bt_api_base.containers.exchanges.exchange_data import ExchangeData
from bt_api_base.logging_factory import get_logger

logger = get_logger("dydx_exchange_data")


class DydxExchangeData(ExchangeData):
    """Base class for all dYdX exchange types.

    Provides shared utility methods (get_symbol, get_period, get_rest_path,
    get_wss_path) and default kline_periods.
    Hardcoded defaults following gateio pattern (no YAML config loading).
    Subclasses MUST set exchange-specific: exchange_name, rest_url, wss_url.
    """

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "DydxSwap"
        self.rest_url = "https://indexer.dydx.trade/v4"
        self.wss_url = "wss://indexer.dydx.trade/v4/ws"
        self.testnet_rest_url = "https://indexer.v4testnet.dydx.exchange/v4"
        self.testnet_wss_url = "wss://indexer.v4testnet.dydx.exchange/v4/ws"

        self.supported_symbols = [
            "BTC-USD",
            "ETH-USD",
            "SOL-USD",
            "ADA-USD",
            "AVAX-USD",
            "DOT-USD",
            "MATIC-USD",
            "LINK-USD",
            "UNI-USD",
            "AAVE-USD",
        ]

        self.rest_paths: dict[str, str] = {
            "get_ticker": "GET /v4/perpetualMarkets",
            "get_perpetual_markets": "GET /v4/perpetualMarkets",
            "get_orderbook": "GET /v4/orderbooks/perpetualMarket/<placeholder>",
            "get_trades": "GET /v4/trades/perpetualMarket/<placeholder>",
            "get_candles": "GET /v4/candles/perpetualMarkets/<placeholder>",
            "get_historical_funding": "GET /v4/historicalFunding/<placeholder>",
            "get_sparklines": "GET /v4/sparklines",
            "get_subaccount": "GET /v4/addresses/<placeholder>/subaccountNumber/<placeholder>",
            "get_orders": "GET /v4/orders",
            "get_fills": "GET /v4/fills",
            "get_funding_payments": "GET /v4/fundingPayments",
            "get_transfers": "GET /v4/transfers",
            "get_historical_pnl": "GET /v4/historical-pnl",
            "get_time": "GET /v4/time",
            "get_markets": "GET /v4/markets",
            "get_exchange_info": "GET /v4/perpetualMarkets",
            "get_market_info": "GET /v4/perpetualMarkets/<placeholder>",
            "get_orderbook_full": "GET /v4/orderbooks/perpetualMarket/<placeholder>?full=true",
            "get_historical_funding_limit": "GET /v4/historicalFunding/<placeholder>?limit=<placeholder>",
        }

        self.wss_paths: dict[str, Any] = {
            "orderbook": {
                "args": [{"channel": "v4_orderbook", "id": "<symbol>"}],
                "op": "subscribe",
            },
            "trades": {
                "args": [{"channel": "v4_trades", "id": "<symbol>"}],
                "op": "subscribe",
            },
            "markets": {"args": [{"channel": "v4_markets"}], "op": "subscribe"},
            "candles": {
                "args": [
                    {
                        "channel": "v4_candles",
                        "id": "<symbol>",
                        "resolution": "<period>",
                    }
                ],
                "op": "subscribe",
            },
            "subaccounts": {
                "args": [
                    {"channel": "v4_subaccounts", "id": "<address>/<subaccount_number>"}
                ],
                "op": "subscribe",
            },
            "parent_subaccounts": {
                "args": [{"channel": "v4_parent_subaccounts", "id": "<address>"}],
                "op": "subscribe",
            },
        }

        self.kline_periods: dict[str, str] = {
            "1m": "1MIN",
            "5m": "5MINS",
            "15m": "15MINS",
            "30m": "30MINS",
            "1h": "1HOUR",
            "4h": "4HOURS",
            "1d": "1DAY",
        }

        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        self.status_dict: dict[str, str] = {
            "open": "open",
            "filled": "filled",
            "canceled": "canceled",
            "expired": "expired",
        }

        self.legal_currency = ["USD", "ETH"]

    def get_symbol(self, symbol: str) -> str:
        """Format trading pair symbol.

        dYdX uses USD as quote currency, convert USDT to USD.
        Also ensures proper formatting with dash separator.
        """
        symbol = symbol.upper()
        if symbol.endswith("USDT"):
            base = symbol[:-4]
            symbol = base + "USD" if base.endswith("-") else base + "-USD"
        elif "-" not in symbol:
            for quote in ["USD", "EUR", "ETH", "BTC"]:
                if symbol.endswith(quote):
                    base = symbol[: -len(quote)]
                    symbol = f"{base}-{quote}"
                    break
        return symbol

    def get_symbol_re(self, symbol: str) -> str:
        """Reverse parse trading pair symbol."""
        return symbol.lower()

    def get_period(self, key: str) -> str:
        """Get kline period."""
        if key not in self.kline_periods:
            return key
        return self.kline_periods[key]

    def get_rest_path(self, key: str, **kwargs) -> str:
        """Get REST API path."""
        if key not in self.rest_paths or self.rest_paths[key] == "":
            self.raise_path_error(self.exchange_name, key)

        path = self.rest_paths[key]
        path = path.replace("<symbol>", "<placeholder>")
        path = path.replace("<address>", "<placeholder>")
        path = path.replace("<subaccount_number>", "<placeholder>")
        path = path.replace("<limit>", "<placeholder>")
        path = path.replace("<resolution>", "<placeholder>")

        return path

    def str2int(self, time_str: str) -> int:
        """Convert time string to timestamp."""
        if time_str.endswith("Z"):
            time_str = time_str[:-1]
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
        timestamp = int((time.mktime(dt.timetuple()) + dt.microsecond / 1000000) * 1000)
        return timestamp

    def get_wss_path(self, **kwargs) -> str:
        """Get WebSocket subscription field."""
        key = kwargs["topic"]
        if key not in self.wss_paths or self.wss_paths[key] == "":
            self.raise_path_error(self.exchange_name, key)

        req = dict(self.wss_paths[key])

        for arg_dict in req.get("args", []):
            for k, v in list(arg_dict.items()):
                if "<symbol>" in v:
                    v = v.replace("<symbol>", kwargs.get("symbol", ""))
                if "<address>" in v:
                    v = v.replace("<address>", kwargs.get("address", ""))
                if "<subaccount_number>" in v:
                    v = v.replace(
                        "<subaccount_number>", str(kwargs.get("subaccount_number", ""))
                    )
                if "<period>" in v:
                    v = v.replace("<period>", self.get_period(kwargs.get("period", "")))
                arg_dict[k] = v

        return json.dumps(req)

    def is_testnet(self) -> bool:
        """Check if using testnet."""
        return self.rest_url == self.testnet_rest_url


class DydxExchangeDataSwap(DydxExchangeData):
    """dYdX perpetual swap."""

    def __init__(self) -> None:
        super().__init__()


class DydxExchangeDataSpot(DydxExchangeData):
    """dYdX spot (if supported)."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "DydxSpot"
