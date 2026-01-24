from ...domain.entities import ExtractDefinition
from ..interfaces import ExtractParamsResolver
from ...domain.params import ExtractParams


class PrepareExtractionParams:
    def __init__(
        self,
        params_resolver: ExtractParamsResolver,
    ):
        self._params_resolver = params_resolver

    def execute(
        self,
        definition: ExtractDefinition,
        config: dict[str, object],
    ) -> ExtractParams:
        return self._params_resolver.resolve(
            definition=definition,
            config=config,
        )
