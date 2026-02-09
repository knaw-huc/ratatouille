import os
import sys

from loguru import logger

from ratatouille.index_merger_config import IndexMergerConfig


def init_logger(show_progress: bool, log_file_path: str):
    if not show_progress:
        logger.remove()
        logger.add(sys.stderr, level="WARNING")

    if log_file_path:
        logger.remove()
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        logger.add(log_file_path)


class IndexMerger:
    def __init__(self, config: IndexMergerConfig):
        init_logger(config.show_progress, config.log_file_path)

        self.errors = []
        self.source_indices = config.source_indices

        if not os.path.exists(config.mapping_path):
            logger.critical(f"Missing mapping file at: {config.mapping_path}")
            sys.exit(1)

    def merge(self):
        logger.info(f"Merging {self.source_indices}")
        return ["example error"]
