import importlib
import pkgutil

from pathlib import Path


def import_all_from_package(package_path: str):
    package = importlib.import_module(package_path)
    package_dir = Path(package.__file__).parent

    if not package_dir.exists():
        raise ValueError(f"Package path does not exist: {package_dir}")

    for module in pkgutil.walk_packages([str(package_dir)], prefix=package_path + "."):
        importlib.import_module(module.name)


def register_all():
    import_all_from_package("app.core.llm_clients")
    import_all_from_package("app.core.agents")
    import_all_from_package("app.core.graphs")
