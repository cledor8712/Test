from __future__ import annotations

import argparse
import time
from pathlib import Path

from gapcli.config import DEFAULT_CONFIG_PATH, init_config, load_config
from gapcli.engine.spread import calculate_spread
from gapcli.exchanges.mock import MockExchange


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gap", description="Crypto gap trading terminal helper")
    sub = parser.add_subparsers(dest="command", required=True)

    config_parser = sub.add_parser("config", help="config commands")
    config_sub = config_parser.add_subparsers(dest="config_command", required=True)
    config_init = config_sub.add_parser("init", help="write default config")
    config_init.add_argument("--path", default=str(DEFAULT_CONFIG_PATH))

    once = sub.add_parser("once", help="calculate one spread snapshot")
    once.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))

    watch = sub.add_parser("watch", help="watch spread repeatedly")
    watch.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    watch.add_argument("--interval", type=float, default=1.0)
    watch.add_argument("--count", type=int, default=10)

    return parser


def _print_result(result) -> None:
    flag = "✅" if result.is_opportunity else "-"
    print(
        f"{flag} gross={result.gross_spread:.4%} net={result.net_spread:.4%} "
        f"buy={result.buy_price:.2f} sell={result.sell_price:.2f}"
    )


def _run_once(config_path: Path) -> int:
    cfg = load_config(config_path)
    buy = MockExchange(cfg.buy_exchange, base_price=100.0)
    sell = MockExchange(cfg.sell_exchange, base_price=101.0)

    buy_ticker = buy.ticker(cfg.pair)
    sell_ticker = sell.ticker(cfg.pair)

    result = calculate_spread(
        buy_price=buy_ticker.ask,
        sell_price=sell_ticker.bid,
        fee_buy=cfg.fee_buy,
        fee_sell=cfg.fee_sell,
        slippage=cfg.slippage,
        transfer_cost=cfg.transfer_cost,
        min_net_spread=cfg.min_net_spread,
    )
    _print_result(result)
    return 0


def _run_watch(config_path: Path, interval: float, count: int) -> int:
    for _ in range(count):
        _run_once(config_path)
        time.sleep(interval)
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "config" and args.config_command == "init":
        path = init_config(Path(args.path))
        print(f"config ready: {path}")
        return 0

    if args.command == "once":
        return _run_once(Path(args.config))

    if args.command == "watch":
        return _run_watch(Path(args.config), args.interval, args.count)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
