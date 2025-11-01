import numpy as np
import pandas as pd

from src.dataset.domain.value_objects import Batch


def append_batches(a: Batch, b: Batch) -> Batch:
    """Combina batches de forma agnóstica ao backend."""

    if a is None:
        return b
    if b is None:
        return a

    X1, X2 = a.X, b.X

    # pandas
    if isinstance(X1, pd.DataFrame):
        merged = pd.concat([X1, X2], ignore_index=True)

    # numpy
    elif isinstance(X1, np.ndarray):
        merged = np.concatenate([X1, X2], axis=0)

    # Fallback genérico
    else:
        raise TypeError(f"Backend não suportado para append: {type(X1)}")

    """
    # PyTorch
    elif "torch" in str(type(X1)):
        import torch
        merged = torch.cat([X1, X2], dim=0)

    # Polars
    elif "polars" in str(type(X1)):
        import polars as pl
        merged = pl.concat([X1, X2])
    """

    # Cria novo Batch preservando demais campos
    return Batch(X=merged, **{k: v for k, v in vars(a).items() if k != "X"})
