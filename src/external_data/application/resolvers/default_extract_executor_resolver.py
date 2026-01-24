from ...domain.entities.extract_definition import ExtractDefinition
from ..errors import ExecutorNotFoundError
from ..interfaces import ExtractExecutor, ExtractExecutorResolver


class DefaultExtractExecutorResolver(ExtractExecutorResolver):
    def __init__(self, executors: list[ExtractExecutor]):
        self._executors = executors

    def resolve(self, definition: ExtractDefinition) -> ExtractExecutor:
        for executor in self._executors:
            if self._matches(executor, definition):
                return executor

        raise ExecutorNotFoundError(
            f"No executor for kind={definition.data_kind} source={definition.source}"
        )

    @staticmethod
    def _matches(
        executor: ExtractExecutor,
        definition: ExtractDefinition,
    ) -> bool:
        return executor.data_kind == definition.data_kind and executor.source == definition.source
