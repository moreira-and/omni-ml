from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.external_data.application.clocks.fixed_clock import FixedClock
from src.external_data.application.errors import ApplicationError
from src.external_data.application.usecases.execute_all_extractions import ExecuteAllExtractions
from src.external_data.application.usecases.execute_batch_extract import ExecuteBatchExtract
from src.external_data.application.usecases.list_extract_definitions import ListExtractDefinitions
from src.external_data.application.usecases.prepare_extraction_params import PrepareExtractionParams
from src.external_data.application.usecases.store_extract_batch import StoreExtractBatch
from src.external_data.domain.entities import ExtractDefinition
from src.external_data.domain.enums import DataKind, ExternalSource, TimeWindow
from src.external_data.domain.models import ExtractBatch
from src.external_data.domain.models.base import DomainModel
from src.external_data.domain.params import TimeRange
from src.external_data.domain.value_objects import DefinitionId, ExternalCode, InternalAlias


@dataclass
class DummyModel(DomainModel):
    value: int


def build_definition() -> ExtractDefinition:
    return ExtractDefinition(
        id=DefinitionId(),
        code=ExternalCode("AAPL"),
        alias=InternalAlias("apple"),
        source=ExternalSource.YFINANCE,
        data_kind=DataKind.CANDLESTICK,
        time_window=TimeWindow.ONE_DAY,
    )


def test_list_extract_definitions_returns_repo_items():
    definition = build_definition()
    repo = MagicMock()
    repo.all.return_value = [definition]

    use_case = ListExtractDefinitions(definitions_repo=repo)

    assert list(use_case.execute()) == [definition]
    repo.all.assert_called_once_with()


def test_prepare_extraction_params_delegates_to_resolver():
    definition = build_definition()
    params = TimeRange(
        start=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end=datetime(2024, 1, 2, tzinfo=timezone.utc),
    )
    resolver = MagicMock()
    resolver.resolve.return_value = params

    use_case = PrepareExtractionParams(params_resolver=resolver)

    result = use_case.execute(definition=definition, config={"start": params.start})

    assert result is params
    resolver.resolve.assert_called_once_with(definition=definition, config={"start": params.start})


def test_execute_batch_extract_builds_batch_and_marks_requested():
    definition = build_definition()
    params = TimeRange(
        start=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end=datetime(2024, 1, 2, tzinfo=timezone.utc),
    )
    model = DummyModel(value=1)
    executor = MagicMock()
    executor.execute.return_value = [model]
    resolver = MagicMock()
    resolver.resolve.return_value = executor
    clock = FixedClock(datetime(2024, 1, 3, tzinfo=timezone.utc))

    use_case = ExecuteBatchExtract(executor_resolver=resolver, clock=clock)

    batch = use_case.execute(definition=definition, params=params)

    assert isinstance(batch, ExtractBatch)
    assert batch.definition is definition
    assert batch.params is params
    assert batch.results == [model]
    assert batch.executed_at == clock.now()
    assert len(definition.pull_events()) == 1
    resolver.resolve.assert_called_once_with(definition)
    executor.execute.assert_called_once_with(definition, params)


def test_store_extract_batch_calls_result_store():
    store = MagicMock()
    batch = MagicMock(spec=ExtractBatch)

    use_case = StoreExtractBatch(result_store=store)

    use_case.execute(batch)

    store.store.assert_called_once_with(batch)


def test_execute_all_extractions_runs_each_definition_and_skips_errors():
    definition_ok = build_definition()
    definition_fail = build_definition()
    params = TimeRange(
        start=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end=datetime(2024, 1, 2, tzinfo=timezone.utc),
    )
    batch = ExtractBatch(
        definition=definition_ok,
        params=params,
        results=[DummyModel(value=1)],
        executed_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
    )

    list_definitions = MagicMock()
    list_definitions.execute.return_value = [definition_ok, definition_fail]
    prepare_params = MagicMock()
    prepare_params.execute.return_value = params
    execute_batch = MagicMock()
    execute_batch.execute.side_effect = [batch, ApplicationError("boom")]
    store_batch = MagicMock()

    use_case = ExecuteAllExtractions(
        list_definitions=list_definitions,
        prepare_params=prepare_params,
        execute_batch=execute_batch,
        store_batch=store_batch,
    )

    use_case.execute({"start": params.start, "end": params.end})

    assert execute_batch.execute.call_count == 2
    store_batch.execute.assert_called_once_with(batch)
