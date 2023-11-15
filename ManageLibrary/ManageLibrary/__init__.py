import importlib
import os
import sys
from pathlib import Path

# To resolve imports for the packaged plugin
# we must insert the root directory
ROOT_DIR = Path(__file__).parent
if ROOT_DIR not in sys.path:
    sys.path.insert(0, str(ROOT_DIR.resolve()))


from ManageView.MLCore import MLCore

import ManageView.ML_Editor.ML_Editor

ML_Core = MLCore()


def initializeSDPlugin():
    ML_Core.initialize_logger()
    ML_Core.add_menu()

    modules_dir = ROOT_DIR / "ManageView"
    for name in os.listdir(modules_dir):
        if not name.startswith("ML_"):
            continue

        try:
            module_path = f"ManageView.{name}.{name}"
            ML_Core.logger.debug(f"Attempting to initialize {module_path}...")
            module = importlib.import_module(module_path)

        except ModuleNotFoundError:
            ML_Core.logger.error(f"Failed to import module {module_path}")
            continue
        else:
            ML_Core.initialize(module)


def uninitializeSDPlugin():
    ML_Core.uninitialize_logger()
    ML_Core.unregister_callbacks()
    ML_Core.remove_toolbars()
    ML_Core.remove_menu()