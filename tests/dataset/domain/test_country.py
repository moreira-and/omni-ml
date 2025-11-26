from datetime import datetime, timedelta, timezone

import pytest

from src.dataset.domain.entities import Country
from src.dataset.domain.value_objects import CountryIndicator
from src.dataset.infrastructure.indicator import BcbIndicator

INTERVAL_DAYS = 30  # janela razoável p/ SELIC
START = datetime.now(tz=timezone.utc) - timedelta(days=INTERVAL_DAYS)
END = datetime.now(tz=timezone.utc)


@pytest.mark.integration
def test_country_aggregate_with_brazil_indicators():
    # 1) Infra: buscar indicadores macroeconômicos do BCB para o país BR
    repo = BcbIndicator()

    indicators = list(
        repo.get_country_indicators(
            country_code="BR",
            name="SELIC",
            start=START,
            end=END,
        )
    )

    # Tem que vir alguma coisa
    assert indicators, "Nenhum indicador retornado para SELIC (BR) na janela configurada."
    assert all(isinstance(i, CountryIndicator) for i in indicators)

    first = indicators[0]
    # Checagens básicas de domínio sobre o VO
    assert first.country_code == "BR"
    assert first.name.upper() == "SELIC"
    assert first.ts.tzinfo is not None and first.ts.utcoffset() is not None

    # Ordenação por timestamp (o adapter deveria manter ordem temporal)
    assert all(a.ts <= b.ts for a, b in zip(indicators, indicators[1:], strict=False))

    # 2) Domínio: construir o agregado Country com esses indicadores
    country = Country(
        code="BR",
        name="BRAZIL",
        indicators=tuple(indicators),
    )

    # 3) Asserções sobre o agregado Country

    # Identidade semântica
    assert country.code == "BR"
    assert country.name == "BRAZIL"

    # Indicadores associados
    assert len(country.indicators) == len(indicators)
    assert all(i.country_code == "BR" for i in country.indicators)

    # Pelo menos um indicador SELIC na coleção
    assert any(i.name == "SELIC" for i in country.indicators)
