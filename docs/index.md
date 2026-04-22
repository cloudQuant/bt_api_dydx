# DYDX Documentation

## English

Welcome to the dYdX documentation for bt_api.

### Quick Start

```bash
pip install bt_api_dydx
```

```python
from bt_api import BtApi

api = BtApi(exchange_kwargs={
    "DYDX___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("DYDX___SPOT", "BTC-USD")
print(ticker)
```

### Supported Operations

| Operation | Exchange Code | Description |
|-----------|---------------|-------------|
| Ticker | `DYDX___SPOT` | Get ticker data |
| OrderBook | `DYDX___SPOT` | Get order book depth |
| Klines | `DYDX___SPOT` | Get candlestick data |
| Trade History | `DYDX___SPOT` | Get recent trades |
| Order | `DYDX___SPOT` | Place/cancel orders |
| Account | `DYDX___SPOT` | Get account info |
| Balance | `DYDX___SPOT` | Get balance info |

## 中文

欢迎使用 bt_api 的 dYdX 文档。

### 快速开始

```bash
pip install bt_api_dydx
```

```python
from bt_api import BtApi

api = BtApi(exchange_kwargs={
    "DYDX___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("DYDX___SPOT", "BTC-USD")
print(ticker)
```

### 支持的操作

| 操作 | 交易所代码 | 说明 |
|------|------------|------|
| Ticker | `DYDX___SPOT` | 获取行情数据 |
| OrderBook | `DYDX___SPOT` | 获取订单簿深度 |
| Klines | `DYDX___SPOT` | 获取K线数据 |
| Trade History | `DYDX___SPOT` | 获取成交历史 |
| Order | `DYDX___SPOT` | 下单/撤单 |
| Account | `DYDX___SPOT` | 获取账户信息 |
| Balance | `DYDX___SPOT` | 获取余额信息 |

## API Reference

See source code in `src/bt_api_dydx/` for detailed API documentation.
