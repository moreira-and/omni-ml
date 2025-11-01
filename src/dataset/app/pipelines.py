from typing import List

from src.config import logger
from src.dataset.domain.interfaces import (  # supondo que sua classe Dataset está neste módulo
    Dataset,
)
from src.dataset.domain.value_objects import Batch
from src.dataset.infra.backend_adapters import append_batches


class PipelineDataset(Dataset):
    """Pipeline composto por múltiplos datasets executados em sequência."""

    def __init__(self, Datasets: List[Dataset] = None) -> None:
        self._stages: List[Dataset] = Datasets

    def add(self, dataset: Dataset) -> "PipelineDataset":
        """Adiciona uma etapa (dataset) ao pipeline."""
        if not isinstance(dataset, Dataset):
            raise TypeError(f"Expected Dataset instance, got {type(dataset).__name__}")
        self._stages.append(dataset)
        return self  # permite encadeamento .add(...).add(...)

    def load(self) -> Batch:
        """Executa todos os datasets em sequência, encadeando os resultados."""
        if not self._stages:
            raise RuntimeError("Pipeline vazio: adicione ao menos um Dataset com .add()")

        result: Batch = None
        for stage in self._stages:
            try:
                batch = stage.load()
                assert not batch.X.empty, f"DataFrame should not be empty. {batch.meta}"
                result = append_batches(result, batch) if result is not None else batch

            except Exception as e:
                logger.warning(f"No data returned: {e}")

        return result
