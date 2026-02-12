from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class Ticker:
    exchange: str
    pair: str
    bid: float
    ask: float


class ExchangeClient(Protocol):
    name: str

    def ticker(self, pair: str) -> Ticker:
        ...
