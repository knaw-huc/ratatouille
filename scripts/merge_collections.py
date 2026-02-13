#!/usr/bin/env python3
from loguru import logger

from ratatouille.index_merger import IndexMerger
from ratatouille.index_merger_config import IndexMergerConfig


def main():
    cf = IndexMergerConfig(
        collections_path="collections.yml",
        show_progress=True,
        # log_file_path="merge_log.txt",
    )
    errors = IndexMerger(cf).merge()
    if errors:
        for error in errors:
            logger.error(error)


if __name__ == "__main__":
    main()
