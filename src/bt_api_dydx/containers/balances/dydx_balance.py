from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class DydxBalanceData(BalanceData):
    """dYdX balance data class."""

    def __init__(
        self,
        balance_info: Any,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "DYDX"
        self.symbol_name = symbol_name
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.address = None
        self.subaccount_number = None
        self.equity = None
        self.free_collateral = None
        self.open_pnl = None
        self.initial_margin_requirement = None
        self.margin_balance = None
        self.available_margin = None
        self.position_margin = None
        self.account_value = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            self.balance_data = json.loads(self.balance_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        balance_data = self.balance_data
        if balance_data is None:
            return self
        if "subaccount" in balance_data:
            subaccount = balance_data["subaccount"]
            self.equity = from_dict_get_float(subaccount, "equity")
            self.free_collateral = from_dict_get_float(subaccount, "freeCollateral")
            self.open_pnl = from_dict_get_float(subaccount, "openPnl")
            self.initial_margin_requirement = from_dict_get_float(
                subaccount, "initialMarginRequirement"
            )
            self.margin_balance = from_dict_get_float(subaccount, "marginBalance")
            self.available_margin = from_dict_get_float(subaccount, "availableMargin")
            self.position_margin = from_dict_get_float(subaccount, "positionMargin")
            self.account_value = from_dict_get_float(subaccount, "accountValue")
        else:
            self.symbol_name = from_dict_get_string(balance_data, "symbol")
            self.equity = from_dict_get_float(balance_data, "equity")
            self.free_collateral = from_dict_get_float(balance_data, "freeCollateral")
            self.open_pnl = from_dict_get_float(balance_data, "unrealizedPnl")
            self.available_margin = from_dict_get_float(balance_data, "availableMargin")
            self.margin_balance = from_dict_get_float(balance_data, "marginBalance")

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "local_update_time": self.local_update_time,
                "asset_type": self.asset_type,
                "address": self.address,
                "subaccount_number": self.subaccount_number,
                "equity": self.equity,
                "free_collateral": self.free_collateral,
                "open_pnl": self.open_pnl,
                "initial_margin_requirement": self.initial_margin_requirement,
                "margin_balance": self.margin_balance,
                "available_margin": self.available_margin,
                "position_margin": self.position_margin,
                "account_value": self.account_value,
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name or ""

    def get_asset_type(self) -> str:
        return self.asset_type or ""

    def get_server_time(self) -> float | None:
        return None

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_account_id(self) -> Any:
        return self.address

    def get_account_type(self) -> Any:
        return "PERPETUAL"

    def get_fee_tier(self) -> Any:
        return None

    def get_max_withdraw_amount(self) -> Any:
        return self.free_collateral

    def get_margin(self) -> Any:
        return self.margin_balance

    def get_used_margin(self) -> Any:
        return self.position_margin

    def get_maintain_margin(self) -> Any:
        return self.initial_margin_requirement

    def get_available_margin(self) -> Any:
        return self.available_margin

    def get_open_order_initial_margin(self) -> Any:
        return self.position_margin

    def get_position_initial_margin(self) -> Any:
        return self.position_margin

    def get_unrealized_profit(self) -> Any:
        return self.open_pnl

    def get_interest(self) -> Any:
        return None

    def get_address(self) -> Any:
        return self.address

    def get_subaccount_number(self) -> Any:
        return self.subaccount_number

    def get_equity(self) -> Any:
        return self.equity

    def get_free_collateral(self) -> Any:
        return self.free_collateral

    def get_account_value(self) -> Any:
        return self.account_value
