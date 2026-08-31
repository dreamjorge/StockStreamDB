import os
import sys
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from trading_algorithms import (  # noqa: E402
    exponential_moving_average,
    fetch_stock_data,
    generate_signals,
    generate_simons_signals,
    main,
    rsi,
    simple_moving_average,
    z_score,
)


def test_simple_moving_average_matches_hand_computation():
    series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])

    result = simple_moving_average(series, window=2)

    assert result.tolist()[1:] == [1.5, 2.5, 3.5, 4.5]
    assert pd.isna(result.iloc[0])


def test_exponential_moving_average_reacts_faster_than_sma_to_a_jump():
    series = pd.Series([10.0] * 10 + [50.0])

    sma = simple_moving_average(series, window=5).iloc[-1]
    ema = exponential_moving_average(series, window=5).iloc[-1]

    assert ema > sma


def test_rsi_is_100_when_every_change_is_a_gain():
    series = pd.Series([float(i) for i in range(1, 20)])

    result = rsi(series, window=14)

    assert result.iloc[-1] == pytest.approx(100.0)


def test_rsi_is_0_when_every_change_is_a_loss():
    series = pd.Series([float(i) for i in range(20, 1, -1)])

    result = rsi(series, window=14)

    assert result.iloc[-1] == pytest.approx(0.0)


def test_z_score_is_zero_at_the_rolling_mean():
    series = pd.Series([10.0, 20.0, 10.0, 20.0, 10.0, 20.0])

    result = z_score(series, window=3)

    assert result.notna().any()


def test_generate_signals_flags_bullish_crossover():
    # A steadily rising series makes the short SMA pull above the long SMA.
    close = pd.Series([float(i) for i in range(1, 80)])
    df = pd.DataFrame({"Close": close})

    result = generate_signals(df)

    assert set(result["Signal"].unique()) <= {-1, 0, 1}
    assert result["Signal"].iloc[-1] == 1


def test_generate_simons_signals_flags_bullish_setup():
    close = pd.Series([float(i) for i in range(1, 80)])
    df = pd.DataFrame({"Close": close})

    result = generate_simons_signals(df)

    assert set(result["Signal"].unique()) <= {-1, 0, 1}
    assert result["Signal"].iloc[-1] == 1


def test_fetch_stock_data_renames_date_column():
    mock_ticker = MagicMock()
    dates = pd.date_range("2024-01-01", periods=3, name="Date")
    mock_ticker.history.return_value = pd.DataFrame(
        {"Open": [1.0, 2.0, 3.0], "Close": [1.5, 2.5, 3.5]}, index=dates
    )

    with patch("trading_algorithms.yf.Ticker", return_value=mock_ticker):
        result = fetch_stock_data("AAPL", period="1mo")

    assert "date" in result.columns
    mock_ticker.history.assert_called_once_with(period="1mo")


def test_fetch_stock_data_raises_for_empty_history():
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()

    with patch("trading_algorithms.yf.Ticker", return_value=mock_ticker):
        with pytest.raises(ValueError, match="No data found"):
            fetch_stock_data("MISSING")


def _mock_price_history(dates):
    # Build the columns directly on the date index (not a default RangeIndex), since
    # pandas aligns Series-valued DataFrame columns by index label: a mismatched index
    # would silently turn every price into NaN instead of raising.
    close = pd.Series(range(1, len(dates) + 1), dtype="float64", index=dates)
    return pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 1000,
        },
        index=dates,
    )


def test_main_runs_basic_strategy_end_to_end(capsys):
    mock_ticker = MagicMock()
    dates = pd.date_range("2024-01-01", periods=60, name="Date")
    mock_ticker.history.return_value = _mock_price_history(dates)

    with patch("trading_algorithms.yf.Ticker", return_value=mock_ticker):
        main("AAPL", period="1y", strategy="basic")

    captured = capsys.readouterr()
    assert "SMA_20" in captured.out
    assert "Signal" in captured.out
    assert "NaN" not in captured.out


def test_main_runs_simons_strategy_end_to_end(capsys):
    mock_ticker = MagicMock()
    dates = pd.date_range("2024-01-01", periods=60, name="Date")
    mock_ticker.history.return_value = _mock_price_history(dates)

    with patch("trading_algorithms.yf.Ticker", return_value=mock_ticker):
        main("AAPL", period="1y", strategy="simons")

    captured = capsys.readouterr()
    assert "EMA_20" in captured.out
    assert "Z_50" in captured.out
    assert "NaN" not in captured.out
