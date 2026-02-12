from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SpreadResult:
    buy_price: float
    sell_price: float
    gross_spread: float
    net_spread: float
    is_opportunity: bool


def calculate_spread(
    *,
    buy_price: float,
    sell_price: float,
    fee_buy: float,
    fee_sell: float,
    slippage: float,
    transfer_cost: float,
    min_net_spread: float,
) -> SpreadResult:
    if buy_price <= 0:
        msg = "buy_price must be positive"
        raise ValueError(msg)

    gross_spread = (sell_price - buy_price) / buy_price
    net_spread = gross_spread - fee_buy - fee_sell - slippage - transfer_cost

    return SpreadResult(
        buy_price=buy_price,
        sell_price=sell_price,
        gross_spread=gross_spread,
        net_spread=net_spread,
        is_opportunity=net_spread >= min_net_spread,
    )
