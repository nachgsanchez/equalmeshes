from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from inspect import isclass

from utils.deps_graph import DepsGraph
from base_classes.registrable import Registrable

import bpy

def register_all_classes():
    classes = gather_all_registrable_classes()
    for c in classes:
        bpy.utils.register_class(c)

def unregister_all_classes():
    classes = gather_all_registrable_classes()
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

def gather_all_registrable_classes():
    root_dir = Path(__file__).parent
    class_set = set()
    _gather_all_registrable_classes(root_dir, class_set, '')
    return DepsGraph.Sorted(class_set)

def _gather_all_registrable_classes(path, class_set, abs_path):
    if abs_path:
        abs_path += '.'

    for (_, modulename, ispkg) in iter_modules([path]):
        module = import_module(abs_path + modulename)
        if ispkg:
            _gather_all_registrable_classes(path.joinpath(modulename), class_set, abs_path + modulename)
        else:
            for att_name in dir(module):
                att = getattr(module, att_name)
                if isclass(att):
                    if (Registrable in att.__bases__):
                        class_set.add(att)