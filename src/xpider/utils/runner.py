from importlib import import_module
from os import getcwd
from pathlib import Path
from sys import path
from xpider.utils import locate_config
import tomlkit

def runner():
    project_root = locate_config(Path(getcwd()), "xpider.toml", file=False)
    if project_root:
        project_file = project_root / "xpider.toml"
        with open(project_file) as project_object:
            project = tomlkit.load(project_object)
            project_name = project["name"]
        path.insert(0, str(project_root / "src"))
        bot_module = import_module(f"{project_name}.main")
        del path[0]
        bot_module.main()