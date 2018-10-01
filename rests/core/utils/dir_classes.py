import importlib
import pkgutil


# =================================
# Find Subclasses in Directory
# ---------------------------------

def find_classes_in_dir(dir_path, pkg, BaseClass) -> dict:
    for (module_loader, name, ispkg) in pkgutil.iter_modules([dir_path]):
        importlib.import_module('.' + name, pkg)

    subclasses = {cls.__name__: cls for cls in BaseClass.__subclasses__()}
    return subclasses