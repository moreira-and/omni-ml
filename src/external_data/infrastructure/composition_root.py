def build_sys_clock():
    from ..application.clocks import SystemClock

    return SystemClock()


def load_extract_config():
    return {"start": "2025-01-01", "end": "2026-01-01"}


def build_definition_repository():
    from .repositories import LocalCsvExtractDefinitionRepository

    return LocalCsvExtractDefinitionRepository()


def build_extractor_resolver():
    from ..application.resolvers import DefaultExtractExecutorResolver

    return DefaultExtractExecutorResolver(build_extract_executors())


def build_extract_param_resolver():
    from ..application.resolvers import DefaultExtractParamsResolver

    return DefaultExtractParamsResolver(build_sys_clock())


def build_result_storage():
    from .storage import LocalCsvResultStorage

    return LocalCsvResultStorage()


def build_extract_executors():
    from .extractors.bcb.time_series import BcbIndicatorExtract
    from .extractors.yfinance.time_series import YFinanceCandleExtract

    return [YFinanceCandleExtract(), BcbIndicatorExtract()]
