from dataclasses import dataclass
from typing import Optional


@dataclass
class IndexMergerConfig:
    source_indices: list[str]
    mapping_path: str
    show_progress: bool = False
    log_file_path: Optional[str] = None
