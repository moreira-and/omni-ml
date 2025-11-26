from datetime import datetime, timedelta, timezone

import pytest

from src.dataset.domain.value_objects import CountryIndicator
from src.dataset.infrastructure.indicator import BcbIndicator


@pytest.mark.integration
def test_bcb_indicator_returns_country_indicator_facts_for_selic():
    repo = BcbIndicator()

    start = datetime.now(tz=timezone.utc) - timedelta(days=5)
    end = datetime.now(tz=timezone.utc)

    indicators = list(
        repo.get_country_indicators(
            country_code="BR",
            name="SELIC",
            start=start,
            end=end,
        )
    )

    assert indicators, "Nenhum indicador retornado para SELIC nos últimos 5 dias."

    first = indicators[0]

    # Tipagem e domínio
    assert isinstance(first, CountryIndicator)
    assert first.country_code == "BR"
    assert first.name.upper() == "SELIC"

    # Semântica temporal
    assert first.ts.tzinfo is not None
    assert first.ts.utcoffset() is not None

    # Ordenação crescente por ts
    assert all(a.ts <= b.ts for a, b in zip(indicators, indicators[1:], strict=False))

    # Valor numérico consistente
    for fact in indicators:
        assert fact.value is not None
