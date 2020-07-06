from pkgutil import iter_modules
from pathlib import Path
from inspect import isclass, ismodule
import importlib
import sys

#This is useful for module reloading when using the 'Reload Scripts' option inside blender
def reload_all_modules():
    root_dir = Path(__file__).parent
    _reload_all_modules(root_dir, '')

def _reload_all_modules(path, module_path):
    if module_path:
        module_path += '.'

    for (_, modulename, ispkg) in iter_modules([path]):
        if ispkg:
            _reload_all_modules(path.joinpath(modulename), module_path + modulename)
        if module_path + modulename in sys.modules:
            importlib.reload(sys.modules[module_path + modulename])
    