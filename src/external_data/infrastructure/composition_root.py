def build_sys_clock():
    from ..application.clocks import SystemClock

    return SystemClock()


def load_extract_config():
    from ...config import read_yaml

    config = read_yaml("config/external_data_params.yaml")
    config_by_kind = {key: value for key, value in config.items()}
    return config_by_kind


def build_definition_repository():
    from .repositories import LocalCsvExtractDefinitionRepository

    return LocalCsvExtractDefinitionRepository()


def build_extractor_resolver():
    from ..application.resolvers import DefaultExtractExecutorResolver

    return DefaultExtractExecutorResolver(build_extract_executors())


def build_extract_param_resolver(clock=None):
    from ..application.resolvers import DefaultExtractParamsResolver

    return DefaultExtractParamsResolver(clock or build_sys_clock())


def build_result_storage():
    from .storage import LocalCsvResultStorage

    return LocalCsvResultStorage()


def build_extract_executors():
    from .extractors.bcb.time_series import BcbIndicatorExtract
    from .extractors.mt5.time_series import MT5CandleExtract
    from .extractors.yfinance.time_series import YFinanceCandleExtract

    return [YFinanceCandleExtract(), BcbIndicatorExtract(), MT5CandleExtract()]
