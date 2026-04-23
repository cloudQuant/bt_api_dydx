from __future__ import annotations

import json
import time

from bt_api_base.containers.orders.order import OrderData, OrderStatus
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class DydxOrderData(OrderData):
    """dYdX order class for determining order properties and methods."""

    def __init__(
        self, order_info, symbol_name, asset_type, has_been_json_encoded=False
    ):
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "DYDX"
        self.symbol_name = symbol_name
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.order_data = self.order_info if has_been_json_encoded else None
        self.server_time = None
        self.order_id = None
        self.client_order_id = None
        self.subaccount_number = None
        self.market = None
        self.side = None
        self.order_type = None
        self.size = None
        self.price = None
        self.reduce_only = None
        self.status = None
        self.created_at = None
        self.updated_at = None
        self.filled_size = None
        self.remaining_size = None
        self.avg_fill_price = None
        self.fees = None
        self.trigger_price = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            self.order_data = json.loads(self.order_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.order_data, list) and self.order_data:
            self.order_data = self.order_data[0]

        if "status" in self.order_data:
            self.status = self.order_data["status"]
            if self.status == "OPEN":
                self.order_status = OrderStatus.ACCEPTED
            elif self.status == "FILLED":
                self.order_status = OrderStatus.COMPLETED
            elif self.status == "CANCELED":
                self.order_status = OrderStatus.CANCELED
            elif self.status == "EXPIRED":
                self.order_status = OrderStatus.EXPIRED
            else:
                self.order_status = OrderStatus.SUBMITTED

        self.server_time = from_dict_get_string(self.order_data, "createdAt")
        self.order_id = from_dict_get_string(self.order_data, "id")
        self.client_order_id = from_dict_get_string(self.order_data, "clientId")
        self.subaccount_number = from_dict_get_string(
            self.order_data, "subaccountNumber"
        )
        self.market = from_dict_get_string(self.order_data, "market")
        self.side = from_dict_get_string(self.order_data, "side")
        self.order_type = from_dict_get_string(self.order_data, "type")
        self.size = from_dict_get_float(self.order_data, "size")
        self.price = from_dict_get_float(self.order_data, "price")
        self.reduce_only = from_dict_get_string(self.order_data, "reduceOnly") == "true"
        self.created_at = from_dict_get_string(self.order_data, "createdAt")
        self.updated_at = from_dict_get_string(self.order_data, "updatedAt")
        self.filled_size = from_dict_get_float(self.order_data, "filledSize")
        self.remaining_size = from_dict_get_float(self.order_data, "remainingSize")
        self.avg_fill_price = from_dict_get_float(self.order_data, "avgFillPrice")
        self.fees = from_dict_get_float(self.order_data, "fees")
        self.trigger_price = from_dict_get_float(self.order_data, "triggerPrice")

        self.has_been_init_data = True
        return self

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "server_time": self.server_time,
                "local_update_time": self.local_update_time,
                "asset_type": self.asset_type,
                "order_id": self.order_id,
                "client_order_id": self.client_order_id,
                "subaccount_number": self.subaccount_number,
                "market": self.market,
                "side": self.side,
                "order_type": self.order_type,
                "size": self.size,
                "price": self.price,
                "reduce_only": self.reduce_only,
                "status": self.status,
                "order_status": self.order_status.value if self.order_status else None,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "filled_size": self.filled_size,
                "remaining_size": self.remaining_size,
                "avg_fill_price": self.avg_fill_price,
                "fees": self.fees,
                "trigger_price": self.trigger_price,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        return self.exchange_name

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_server_time(self):
        return self.server_time

    def get_local_update_time(self):
        return self.local_update_time

    def get_trade_id(self):
        return self.order_id

    def get_client_order_id(self):
        return self.client_order_id

    def get_cum_quote(self):
        return None

    def get_executed_qty(self):
        return self.filled_size

    def get_order_id(self):
        return self.order_id

    def get_order_size(self):
        return self.size

    def get_order_price(self):
        return self.price

    def get_reduce_only(self):
        return self.reduce_only

    def get_order_side(self):
        return self.side

    def get_order_status(self):
        return self.order_status

    def get_trailing_stop_price(self):
        return None

    def get_trailing_stop_trigger_price(self):
        return None

    def get_trailing_stop_trigger_price_type(self):
        return None

    def get_trailing_stop_callback_rate(self):
        return None

    def get_order_symbol_name(self):
        return self.market

    def get_order_time_in_force(self):
        return self.order_type

    def get_order_type(self):
        return self.order_type

    def get_order_avg_price(self):
        return self.avg_fill_price

    def get_origin_order_type(self):
        return self.order_type

    def get_position_side(self):
        return "BOTH" if not self.reduce_only else "REDUCE_ONLY"

    def get_close_position(self):
        return None

    def get_take_profit_price(self):
        return None

    def get_take_profit_trigger_price(self):
        return None

    def get_take_profit_trigger_price_type(self):
        return None

    def get_stop_loss_price(self):
        return self.trigger_price

    def get_stop_loss_trigger_price(self):
        return self.trigger_price

    def get_stop_loss_trigger_price_type(self):
        return None

    def get_subaccount_number(self):
        return self.subaccount_number
