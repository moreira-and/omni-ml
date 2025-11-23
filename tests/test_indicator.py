from datetime import datetime, timedelta

import pytest

from src.dataset.infrastructure.indicator import BcbIndicator


@pytest.mark.integration
def test_BcbIndicator():

    repo = BcbIndicator()

    indicators = list(
        repo.get_indicator(
            name="SELIC",
            start=datetime.today() - timedelta(days=5),
            end=datetime.today(),
        )
    )

    print(indicators)

    assert len(indicators) > 0
    first = indicators[0]
