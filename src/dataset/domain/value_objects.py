from dataclasses import dataclass
from typing import Any, Dict, Optional


# === Tipos de dados ===
@dataclass(frozen=True)
class Batch:
    X: Any  # ex.: pd.DataFrame/np.ndarray/torch.Tensor
    meta: Optional[Dict[str, Any]] = None
