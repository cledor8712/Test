from __future__ import annotations

import random

from .base import Ticker


class MockExchange:
    def __init__(self, name: str, base_price: float) -> None:
        self.name = name
        self.base_price = base_price

    def ticker(self, pair: str) -> Ticker:
        # 작은 랜덤 흔들림을 주어 watch 모드에서 기회 탐지 테스트가 가능하도록 함.
        mid = self.base_price * random.uniform(0.998, 1.002)
        spread = mid * 0.0005
        return Ticker(exchange=self.name, pair=pair, bid=mid - spread, ask=mid + spread)
