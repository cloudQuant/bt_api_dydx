"""Tests for bt_api_dydx plugin registration."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.loader import PluginLoader
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry
from bt_api_py.testing import create_isolated_exchange_registry, reset_gateway_runtime_registrar

from bt_api_dydx.plugin import register_plugin


@dataclass
class _EntryPoint:
    name: str = "dydx"
    module: str = "bt_api_dydx.plugin"

    def load(self) -> Any:
        module = import_module(self.module)
        return module.register_plugin


class _RuntimeFactory:
    def __init__(self) -> None:
        self.adapters: dict[str, type[Any]] = {}

    def register_adapter(self, exchange_type: str, adapter_cls: type[Any]) -> None:
        self.adapters[exchange_type] = adapter_cls


def setup_function() -> None:
    ExchangeRegistry.clear()
    reset_gateway_runtime_registrar()


def test_register_plugin_returns_plugin_info():
    runtime_factory = _RuntimeFactory()
    registry = create_isolated_exchange_registry()
    info = register_plugin(registry, runtime_factory)

    assert isinstance(info, PluginInfo)
    assert info.name == "bt_api_dydx"
    assert info.version == "0.15.0"
    assert info.supported_exchanges == ("DYDX___SPOT", "DYDX___SWAP")
    assert info.supported_asset_types == ("SPOT", "SWAP")
    assert registry.get_feed_class("DYDX___SPOT") is not None
    assert registry.get_feed_class("DYDX___SWAP") is not None
    assert "DYDX" not in runtime_factory.adapters


def test_plugin_loader_loads_dydx_plugin(monkeypatch):
    loader = PluginLoader(ExchangeRegistry, GatewayRuntimeRegistrar)
    monkeypatch.setattr(loader, "_discover_entry_points", lambda group: [_EntryPoint()])

    loader.load_all()

    assert "bt_api_dydx" in loader.loaded
    assert loader.loaded["bt_api_dydx"].plugin_module == "bt_api_dydx.plugin"
    assert ExchangeRegistry.get_feed_class("DYDX___SPOT") is not None
    assert ExchangeRegistry.get_feed_class("DYDX___SWAP") is not None
