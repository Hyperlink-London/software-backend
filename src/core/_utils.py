import os

from .constants import DEV_MODE_ENV_VAR_NAME


def dev_mode_active() -> bool:
    try:
        if os.environ[DEV_MODE_ENV_VAR_NAME] == '1':
            return True
        else:
            return False
    except KeyError:
        set_dev_mode(False)
        return False


def set_dev_mode(mode: bool) -> None:
    dev_mode = '1' if mode is True else '0'
    os.environ[DEV_MODE_ENV_VAR_NAME] = dev_mode
