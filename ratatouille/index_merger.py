import os
import sys
from pathlib import Path

import yaml
from elasticsearch8 import Elasticsearch
from elasticsearch8.helpers import scan
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
            self.target_es = Elasticsearch([self.target_url])

            p = config["target"]["mapping"]
            if not os.path.exists(p):
                logger.critical(f"Missing target index file at: {p}")
                sys.exit(1)
            logger.info(f"Loading target index mapping from: {p}")
            self.target_mapping = Path(p).read_text(encoding="utf-8")

            self.setup_target_index()

    def setup_target_index(self):
        logger.info(f"Setting up Elasticsearch index on {self.target_url}")
        es = self.target_es
        if es.indices.exists(index=self.target_index):
            logger.warning(f"Deleting existing index: {self.target_index}")
            es.indices.delete(index=self.target_index)
        logger.info(f"Creating index: {self.target_index}")
        es.indices.create(index=self.target_index, body=self.target_mapping)

    def merge(self):
        source_names = [s["index"] for s in self.sources]
        logger.info(f"Merging {source_names} into '{self.target_index}'")
        for s in self.sources:
            self.merge_source(s)
        return ["example error"]

    def merge_source(self, src_conf):
        source_es = Elasticsearch(src_conf["url"])
        doc_generator = scan(
            source_es,
            index=src_conf["index"],
            query={"query": {"match_all": {}}},
            scroll="5m",  # Keep the search context alive for 5 minutes
        )
        count = 0
        for src_doc in doc_generator:
            # Each 'src_doc' is a dictionary containing metadata and the source
            src_doc_id = src_doc["_id"]
            src_data = src_doc["_source"]
            src_vars = {
                "index": src_conf["index"],
                "url": src_conf["url"],
            }

            logger.info(f"Processing: {src_doc_id}")

            doc = {}
            for field in src_conf["fields"]:
                source_field_name = field.get("source")
                target_field_name = field.get("target") or source_field_name

                if source_field_name:
                    value = src_data.get(source_field_name)
                    if not value:
                        logger.warning(f"No {source_field_name} in {src_doc_id}")
                        continue
                else:
                    value = None

                if "lambda" in field:
                    fn = eval("lambda " + field["lambda"], src_vars, {})
                    value = fn(value)

                if target_field_name:
                    doc[target_field_name] = value
                else:
                    logger.error(f"No target for {field} in: {src_doc_id}")
                    continue

            self.target_es.index(index=self.target_index, id=src_doc_id, document=doc)
