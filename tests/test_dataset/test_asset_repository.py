import pytest

from src.dataset.domain.enums import CandleInterval

from .test_fixture import asset_repository, sample_asset


def test_save_and_get_by_symbol(
    sample_asset,
    asset_repository,
):
    symbol = "^BVSP"
    # act
    asset_repository.save(sample_asset)
    assets = list(asset_repository.get_by_symbol(symbol))

    # assert (asset)
    assert len(assets) == 1
    asset = assets[0]
    assert asset.symbol == symbol

    # assert (candles)
    candles = list(asset.candles)
    assert len(candles) == 2

    assert candles[0].open == 10.0
    assert candles[1].close == 12.0
    assert candles[0].interval == CandleInterval.ONE_DAY

    # cleanup
    asset_repository.delete_by_symbol(symbol)
