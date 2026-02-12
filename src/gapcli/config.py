from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


DEFAULT_CONFIG_PATH = Path("gapcli.config.json")


@dataclass(slots=True)
class GapConfig:
    buy_exchange: str = "upbit"
    sell_exchange: str = "binance"
    pair: str = "BTC/USDT"
    fee_buy: float = 0.0005
    fee_sell: float = 0.0005
    slippage: float = 0.001
    transfer_cost: float = 0.0005
    min_net_spread: float = 0.008


def init_config(path: Path = DEFAULT_CONFIG_PATH) -> Path:
    if path.exists():
        return path

    path.write_text(json.dumps(asdict(GapConfig()), indent=2), encoding="utf-8")
    return path


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> GapConfig:
    if not path.exists():
        return GapConfig()

    data = json.loads(path.read_text(encoding="utf-8"))
    return GapConfig(**data)
