# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2025 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
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
