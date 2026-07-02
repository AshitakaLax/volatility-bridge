python\_package.volatile\_models package
====================================

Submodules
----------

python\_package.volatile\_models.volatile\_models module
------------------------------------------------

Models
------
### 1. INTERNAL SYSTEM MODELS

#### SellInstruction

*   Description: Instructs the OMS to sell a specific fractional or full quantity of an open lot.
*   Attributes:
    +   lot_id (str)
    +   qty (float)

#### StrategySignal

*   Description: The master signal returned by a Sizing Strategy to the OMS.
*   Attributes:
    +   execute_buy (bool)
    +   trade_value (float)
    +   grid_step (float)
    +   profit_target (float)
    +   sell_instructions (List[SellInstruction])

### 2. BACKEND ➔ UI MODELS

#### DashboardLot

*   Description: Strictly typed schema for an active inventory lot displayed on the UI.
*   Attributes:
    +   lot_id (str)
    +   buy_price (float)
    +   target_sell_price (float)
    +   shares (float)
    +   timestamp (Optional[datetime])

#### DashboardStatePayload

*   Description: The master data contract sent FROM the backend TO the Streamlit UI.
*   Attributes:
    +   message_type (Literal["state_update"])
    +   symbol (str)
    +   current_price (float)
    +   last_buy_price (float)
    +   grid_step (float)
    +   open_lots (List[DashboardLot])
    +   closed_lots_count (int)
    +   realized_profit (float)
    +   timestamp (datetime)

### 3. UI ➔ BACKEND MODELS

#### UICommandEmergencyHalt

*   Description: Command to pause all new buy orders (sells remain active to harvest).
*   Attributes:
    +   command (Literal["emergency_halt"])

#### UICommandResumeTrading

*   Description: Command to resume normal algorithmic trading.
*   Attributes:
    +   command (Literal["resume_trading"])

#### UICommandLiquidateAll

*   Description: Command to instantly cancel open orders and market-sell all inventory.
*   Attributes:
    +   command (Literal["liquidate_all"])

#### UICommandUpdateConfig

*   Description: Command to dynamically adjust grid or profit parameters on the fly.
*   Attributes:
    +   command (Literal["update_config"])
    +   new_grid_step (Optional[float])
    +   new_profit_target (Optional[float])

#### UICommandMessage

*   Description: A unified type to easily parse any incoming command from the WebSocket.
*   Type: Union[UICommandEmergencyHalt, UICommandResumeTrading, UICommandLiquidateAll, UICommandUpdateConfig]

.. automodule:: volatility-bridge.volatile_models
   :members:
   :undoc-members:
   :show-inheritance:
