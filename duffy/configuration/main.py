from itertools import chain
from pathlib import Path
from typing import List, Union

import yaml

from ..util import merge_dicts
from .validation import ConfigModel

config = {}


def _expand_normalize_config_files(config_files: List[Union[Path, str]]) -> List[Path]:
    config_file_paths = []

    for path in config_files:
        if not isinstance(path, Path):
            path = Path(path)
        if path.is_dir():
            config_file_paths.extend(sorted(chain(path.glob("*.yaml"), path.glob("*.yml"))))
        else:
            config_file_paths.append(path)

    return config_file_paths


def read_configuration(
    *config_files: List[Union[Path, str]], clear: bool = True, validate: bool = True
):
    config_files = _expand_normalize_config_files(config_files)
    new_config = {}
    for config_file in config_files:
        with config_file.open("r") as fp:
            for config_doc in yaml.safe_load_all(fp):
                new_config = merge_dicts(new_config, config_doc)

    if validate:
        # validate merged configuration
        ConfigModel(**new_config)

    if clear:
        config.clear()

    config.update(new_config)
