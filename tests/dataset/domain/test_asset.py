from datetime import datetime, timedelta, timezone

import pytest

from src.dataset.domain.entities import Asset
from src.dataset.domain.value_objects import AssetListing, AssetPrice
from src.dataset.infrastructure.price import YfinancePrice

PETRO_SYMBOL = "PETR4.SA"
PETRO_NAME = "Petróleo Brasileiro S.A. - Petrobras"
INTERVAL = "1d"
START = datetime.now(tz=timezone.utc) - timedelta(days=5)
END = datetime.now(tz=timezone.utc)


@pytest.mark.integration
def test_asset_aggregate_with_prices_for_petrobras():
    # 1) Infra: buscar preços via YfinancePrice
    price_repo = YfinancePrice()

    prices = list(
        price_repo.get_prices(
            symbol=PETRO_SYMBOL,
            interval=INTERVAL,
            start=START,
            end=END,
        )
    )

    assert prices, "Nenhum preço retornado para PETR4.SA nos últimos 5 dias."
    assert all(isinstance(p, AssetPrice) for p in prices)

    first_price = prices[0]
    # Garante que o VO de domínio veio coerente com o symbol
    assert first_price.listing.symbol == PETRO_SYMBOL.upper()

    # 2) Domínio: construir o agregado Asset e associar os preços

    petro_listing = AssetListing(
        symbol=PETRO_SYMBOL.upper(),
        exchange="B3",
        currency="BRL",
    )

    asset = Asset(
        name=PETRO_NAME,
        listings=(petro_listing,),
        country_code="BR",
        prices=tuple(prices),
        indicators=tuple(),
    )

    # 3) Asserções de domínio sobre o agregado

    # Asset com nome correto
    assert asset.name == PETRO_NAME

    # País correto
    assert asset.country_code == "BR"

    # Pelo menos uma listing e ela é a da Petrobras na B3
    assert len(asset.listings) == 1
    assert asset.listings[0].symbol == PETRO_SYMBOL.upper()
    assert asset.listings[0].exchange == "B3"
    assert asset.listings[0].currency == "BRL"

    # Preços foram atribuídos ao agregado
    assert len(asset.prices) == len(prices)
    # Todas as barras com o mesmo symbol da Petrobras
    assert all(p.listing.symbol == PETRO_SYMBOL.upper() for p in asset.prices)
