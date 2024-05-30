"""
Module to connect a Python interpreter (including from a DCC like Maya, Blender etc) to a running
[PyCharm remote debugging server](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config).

Start a remote debug configuration and run this in the target Python interpreter.

    .. code-block:: python

        >>> import pycharm_debug
        >>> pycharm_debug.start(port=7520)
        True

If a `pydevd` module is not yet discoverable for import, the latest PyCharm install is used instead.
This convenience allows developers to frequently update PyCharm without needing to re-add the new install
location for pydevd.

"""
import importlib
import logging
import os
import pkgutil
import re
import sys

try:
    import winreg
except ImportError:
    import _winreg as winreg


logging.basicConfig()
LOGGER = logging.getLogger('pycharm_debug')

_NUMBER_PATTERN = re.compile(r'\d+')

MODULE_NAME = 'pydevd'

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 7200


def _num_sort_key(value):
    return list(map(int, _NUMBER_PATTERN.findall(value)))[0]


def get_pydevd_location():
    """
    Get application install directories for PyCharm.
    :return str|None: pydevd module directory, if found.
    """
    # Attempt to get from available module locations
    for mod_path, name, _ in pkgutil.iter_modules(prefix=MODULE_NAME):
        if name == MODULE_NAME:
            LOGGER.debug('Found {} directory from available modules "{}".'.format(MODULE_NAME, mod_path))
            return mod_path.path

    # Get from PyCharm install directory

    # if sys.platform.startswith("win"):
    reg_path = r'SOFTWARE\WOW6432Node\JetBrains\PyCharm'

    directories = []
    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as reg:
        with winreg.OpenKey(reg, reg_path) as key:
            for i in range(1024):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    directories.append(winreg.QueryValueEx(subkey, None)[0])
                except EnvironmentError:
                    break

    # Paths changes in PyCharm versions
    relative_path_variations = (
        ('helpers', 'pydev'),
        ('plugins', 'python', 'helpers', 'pydev'),
    )

    # Sort in reverse to ensure the results are in descending version order (newest first).
    for directory in sorted(directories, reverse=True, key=_num_sort_key):
        for rel_path_variant in relative_path_variations:
            path = os.path.join(directory, *rel_path_variant)
            if os.path.isdir(path):
                LOGGER.debug('Found {} directory "{}".'.format(MODULE_NAME, path))
                return path

    return None


def setup(pydevd_path=None):
    """
    Setup debugging.
    :param str|None pydevd_path: pydevd module path to use. Find most relevant
        path if None given.
    """
    # Check if module is already available for import.
    try:
        importlib.import_module(MODULE_NAME)
        return True
    except ImportError:
        pass

    pydevd_path = pydevd_path or get_pydevd_location()
    if not pydevd_path:
        return False

    # Use the given path
    if pydevd_path not in sys.path:
        sys.path.append(pydevd_path)

    return True


def start(port=DEFAULT_PORT, host=DEFAULT_HOST):
    """
    Start the python debugger and set tracing to <port> and <host>.
    :param int port: Port number to use.
    :param str host: Host to use.
    :return bool: True if connection was successful.
    """
    try:
        setup()
        mod = importlib.import_module(MODULE_NAME)
    except ImportError as e:
        LOGGER.error('Failed to import "{}" :: {}'.format(MODULE_NAME, e))
        return False
    except RuntimeError as e:
        LOGGER.error('Failure occurred during setup and import of "{}" :: {}'.format(MODULE_NAME, e))
        return False

    # Close existing connections (if you've restarted debugger from PyCharm)
    mod.stoptrace()
    mod.settrace(
        host,
        port=port,
        stdoutToServer=True,
        stderrToServer=True,
        suspend=False,
    )
    LOGGER.info('PyCharm connection made to {}:{}'.format(host, port))
    return True
