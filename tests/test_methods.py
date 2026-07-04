#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

from volatility_bridge.volatile_models import (
    SellInstruction,
    StrategySignal,
    DashboardLot,
    DashboardStatePayload,
    UICommandEmergencyHalt,
    UICommandResumeTrading,
    UICommandLiquidateAll,
    UICommandUpdateConfig,
)
from datetime import datetime
import pytest


@pytest.mark.integration
def test_internal_models():
    """Test validation and attribute access for internal trading models."""
    sell = SellInstruction(lot_id="lot_01", qty=2.5)
    assert sell.lot_id == "lot_01"
    assert sell.qty == 2.5

    signal = StrategySignal(
        execute_buy=True,
        trade_value=500.0,
        grid_step=0.015,
        profit_target=0.03,
        sell_instructions=[sell],
    )
    assert signal.execute_buy is True
    assert len(signal.sell_instructions) == 1
    assert signal.sell_instructions[0].lot_id == "lot_01"


def test_dashboard_models():
    """Test validation and structure of backend-to-UI telemetry models."""
    lot = DashboardLot(
        lot_id="lot_02",
        buy_price=100.0,
        target_sell_price=103.0,
        shares=10.0,
        timestamp=datetime(2026, 7, 3, 12, 0, 0),
    )
    assert lot.lot_id == "lot_02"
    assert lot.buy_price == 100.0

    payload = DashboardStatePayload(
        symbol="BTCUSD",
        current_price=101.5,
        last_buy_price=100.0,
        grid_step=0.015,
        open_lots=[lot],
        closed_lots_count=5,
        realized_profit=250.0,
        timestamp=datetime(2026, 7, 3, 12, 0, 1),
    )
    assert payload.symbol == "BTCUSD"
    assert len(payload.open_lots) == 1


def test_ui_commands():
    """Test parsing and creation of UI-to-backend command models."""
    halt = UICommandEmergencyHalt(command="emergency_halt")
    assert halt.command == "emergency_halt"

    resume = UICommandResumeTrading(command="resume_trading")
    assert resume.command == "resume_trading"

    liquidate = UICommandLiquidateAll(command="liquidate_all")
    assert liquidate.command == "liquidate_all"

    update = UICommandUpdateConfig(
        command="update_config",
        new_grid_step=0.02,
        new_profit_target=0.04,
    )
    assert update.command == "update_config"
    assert update.new_grid_step == 0.02
    assert update.new_profit_target == 0.04
