"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class DydxTickerData(TickerData):
    """dYdX ticker information."""

    def __init__(
        self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "DYDX"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded else None
        )
        self.ticker_symbol_name: str | None = None
        self.has_been_init_data = False
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.server_time: float | str | None = None
        self.last_price: float | None = None
        self.last_volume: float | None = None
        self.high_24h: float | None = None
        self.low_24h: float | None = None
        self.volume_24h: float | None = None
        self.volume_24h_usd: float | None = None
        self.funding_rate: float | None = None
        self.next_funding_rate: float | None = None
        self.next_funding_at: str | None = None
        self.mark_price: float | None = None
        self.oracle_price: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        """init_data method"""
        raise NotImplementedError

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "ticker_symbol_name": self.ticker_symbol_name,
                "server_time": self.server_time,
                "last_price": self.last_price,
                "last_volume": self.last_volume,
                "high_24h": self.high_24h,
                "low_24h": self.low_24h,
                "volume_24h": self.volume_24h,
                "volume_24h_usd": self.volume_24h_usd,
                "funding_rate": self.funding_rate,
                "next_funding_rate": self.next_funding_rate,
                "next_funding_at": self.next_funding_at,
                "mark_price": self.mark_price,
                "oracle_price": self.oracle_price,
            }
        return self.all_data or {}

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return str(self.exchange_name)

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return float(self.local_update_time)

    def get_symbol_name(self) -> str:
        """get_symbol_name method"""
        return str(self.symbol_name)

    def get_ticker_symbol_name(self) -> str | None:
        """get_ticker_symbol_name method"""
        val = self.ticker_symbol_name
        return None if val is None else str(val)

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return str(self.asset_type)

    def get_server_time(self) -> float | None:
        """get_server_time method"""
        st = self.server_time
        if st is None:
            return None
        if isinstance(st, (int, float)):
            return float(st)
        try:
            return float(st)
        except (TypeError, ValueError):
            return None

    def get_last_price(self) -> float | None:
        """get_last_price method"""
        return self.last_price

    def get_last_volume(self) -> float | None:
        """get_last_volume method"""
        return self.last_volume

    def get_high_24h(self) -> float | None:
        """get_high_24h method"""
        return self.high_24h

    def get_low_24h(self) -> float | None:
        """get_low_24h method"""
        return self.low_24h

    def get_volume_24h(self) -> float | None:
        """get_volume_24h method"""
        return self.volume_24h

    def get_volume_24h_usd(self):
        """get_volume_24h_usd method"""
        return self.volume_24h_usd

    def get_funding_rate(self):
        """get_funding_rate method"""
        return self.funding_rate

    def get_next_funding_rate(self):
        """get_next_funding_rate method"""
        return self.next_funding_rate

    def get_next_funding_at(self):
        """get_next_funding_at method"""
        return self.next_funding_at

    def get_mark_price(self):
        """get_mark_price method"""
        return self.mark_price

    def get_oracle_price(self):
        """get_oracle_price method"""
        return self.oracle_price


class DydxWssTickerData(DydxTickerData):
    """dYdX WebSocket ticker information."""

    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        ticker_data = self.ticker_data or {}
        if "markets" in ticker_data:
            markets = ticker_data["markets"]
            if isinstance(markets, dict) and self.symbol_name in markets:
                market_data = markets[self.symbol_name]
                self.last_price = from_dict_get_float(market_data, "oraclePrice")
                self.volume_24h = from_dict_get_float(market_data, "volume24H")
                self.funding_rate = from_dict_get_float(
                    market_data, "currentFundingRate"
                )
                self.next_funding_at = from_dict_get_string(
                    market_data, "nextFundingRateAt"
                )

        self.has_been_init_data = True
        return self


class DydxRequestTickerData(DydxTickerData):
    """dYdX REST API ticker information."""

    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        ticker_data = self.ticker_data or {}
        if "markets" in ticker_data:
            markets = ticker_data["markets"]
            if isinstance(markets, dict) and self.symbol_name in markets:
                market_data = markets[self.symbol_name]
                self.ticker_symbol_name = self.symbol_name
                self.server_time = from_dict_get_string(market_data, "snapshotAt")
                self.last_price = from_dict_get_float(market_data, "oraclePrice")
                self.volume_24h = from_dict_get_float(market_data, "volume24H")
                self.volume_24h_usd = from_dict_get_float(
                    market_data, "volumeNotional24H"
                )
                self.high_24h = from_dict_get_float(market_data, "high24H")
                self.low_24h = from_dict_get_float(market_data, "low24H")
                self.funding_rate = from_dict_get_float(
                    market_data, "currentFundingRate"
                )
                self.next_funding_at = from_dict_get_string(
                    market_data, "nextFundingRateAt"
                )
                self.mark_price = from_dict_get_float(market_data, "markPrice")
                self.oracle_price = from_dict_get_float(market_data, "oraclePrice")

        self.has_been_init_data = True
        return self
