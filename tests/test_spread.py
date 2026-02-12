from gapcli.engine.spread import calculate_spread


def test_calculate_spread_marks_opportunity() -> None:
    result = calculate_spread(
        buy_price=100,
        sell_price=102,
        fee_buy=0.001,
        fee_sell=0.001,
        slippage=0.001,
        transfer_cost=0.001,
        min_net_spread=0.01,
    )

    assert round(result.gross_spread, 3) == 0.02
    assert result.is_opportunity is True


def test_calculate_spread_rejects_invalid_price() -> None:
    try:
        calculate_spread(
            buy_price=0,
            sell_price=100,
            fee_buy=0.001,
            fee_sell=0.001,
            slippage=0.001,
            transfer_cost=0.001,
            min_net_spread=0.01,
        )
    except ValueError as exc:
        assert "buy_price" in str(exc)
    else:
        raise AssertionError("ValueError expected")
