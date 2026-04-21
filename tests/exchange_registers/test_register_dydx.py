"""Tests for exchange_registers/register_dydx.py."""

from __future__ import annotations

from bt_api_dydx.registry_registration import register_dydx


class TestRegisterDydx:
    """Tests for dYdX registration module."""

    def test_module_imports(self):
        """Test module can be imported."""
        assert register_dydx is not None
