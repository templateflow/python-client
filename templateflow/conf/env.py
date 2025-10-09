import os
from functools import partial
from pathlib import Path
from typing import Callable

from platformdirs import user_cache_dir


def _env_to_bool(envvar: str, default: bool) -> bool:
    """Check for environment variable switches and convert to booleans."""
    switches = {
        'on': {'true', 'on', '1', 'yes', 'y'},
        'off': {'false', 'off', '0', 'no', 'n'},
    }

    val = os.getenv(envvar, default)
    if isinstance(val, str):
        if val.lower() in switches['on']:
            return True
        elif val.lower() in switches['off']:
            return False
        else:
            # TODO: Create templateflow logger
            print(
                f'{envvar} is set to unknown value <{val}>. '
                f'Falling back to default value <{default}>'
            )
            return default
    return bool(val)


def get_templateflow_home() -> Path:
    return Path(os.getenv('TEMPLATEFLOW_HOME', user_cache_dir('templateflow'))).absolute()


def env_to_bool(envvar: str, default: bool) -> Callable[[], bool]:
    return partial(_env_to_bool, envvar, default)
