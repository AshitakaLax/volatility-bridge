from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union
from datetime import datetime

# ==========================================
# 1. INTERNAL SYSTEM MODELS
#    Used strictly within the backend trading loop
# ==========================================


class SellInstruction(BaseModel):
    """Instructs the OMS to sell a specific fractional or full quantity of an open lot."""

    lot_id: str
    qty: float


class StrategySignal(BaseModel):
    """The master signal returned by a Sizing Strategy to the OMS."""

    execute_buy: bool
    trade_value: float
    grid_step: float
    profit_target: float
    sell_instructions: List[SellInstruction] = Field(default_factory=list)


# ==========================================
# 2. BACKEND ➔ UI MODELS
#    Outbound telemetry payload sent to the Streamlit Dashboard
# ==========================================


class DashboardLot(BaseModel):
    """Strictly typed schema for an active inventory lot displayed on the UI."""

    lot_id: str
    buy_price: float
    target_sell_price: float
    shares: float
    timestamp: Optional[datetime] = None


class DashboardStatePayload(BaseModel):
    """The master data contract sent FROM the backend TO the Streamlit UI."""

    message_type: Literal["state_update"] = "state_update"
    symbol: str
    current_price: float
    last_buy_price: float
    grid_step: float
    open_lots: List[DashboardLot] = Field(default_factory=list)
    closed_lots_count: int
    realized_profit: float
    timestamp: datetime


# ==========================================
# 3. UI ➔ BACKEND MODELS
#    Inbound commands sent from the Streamlit Dashboard to Main.py
# ==========================================


class UICommandEmergencyHalt(BaseModel):
    """Command to pause all new buy orders (sells remain active to harvest)."""

    command: Literal["emergency_halt"]


class UICommandResumeTrading(BaseModel):
    """Command to resume normal algorithmic trading."""

    command: Literal["resume_trading"]


class UICommandLiquidateAll(BaseModel):
    """Command to instantly cancel open orders and market-sell all inventory."""

    command: Literal["liquidate_all"]


class UICommandUpdateConfig(BaseModel):
    """Command to dynamically adjust grid or profit parameters on the fly."""

    command: Literal["update_config"]
    new_grid_step: Optional[float] = None
    new_profit_target: Optional[float] = None


# A unified type to easily parse any incoming command from the WebSocket
UICommandMessage = Union[UICommandEmergencyHalt, UICommandResumeTrading, UICommandLiquidateAll, UICommandUpdateConfig]
