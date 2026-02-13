from dataclasses import dataclass
from typing import Optional


@dataclass
class IndexMergerConfig:
    collections_path: str
    show_progress: bool = False
    log_file_path: Optional[str] = None
