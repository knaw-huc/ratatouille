import os
import sys
from pathlib import Path

import yaml
from elasticsearch8 import Elasticsearch
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

        if not os.path.exists(config.collections_path):
            logger.critical(f"Missing file at: {config.collections_path}")
            sys.exit(1)

        with open(config.collections_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)

            # setup sources config
            self.sources = config["sources"]

            # setup target config
            self.target_index = config["target"]["index"]
            self.target_url = config["target"]["url"]

            p = config["target"]["mapping"]
            if not os.path.exists(p):
                logger.critical(f"Missing target index file at: {p}")
                sys.exit(1)
            logger.info(f"Loading target index mapping from: {p}")
            self.target_mapping = Path(p).read_text(encoding="utf-8")

            self.validate()

    def validate(self):
        es = Elasticsearch([self.target_url])
        if es.indices.exists(index=self.target_index):
            logger.warning(f"Target index {self.target_index} exists")
            es.indices.delete(index=self.target_index)
        es.indices.create(index=self.target_index, body=self.target_mapping)

    def merge(self):
        source_names = [s["index"] for s in self.sources]
        logger.info(f"Merging {source_names} into {self.target_index}")
        return ["example error"]
