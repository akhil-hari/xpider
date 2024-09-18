from importlib import import_module
from os import getcwd
from pathlib import Path
from sys import path
from xpider.utils.locate_config import locate_config
import tomlkit
from xpider.processor.process_loop import ProcessLoop

def runner():
    project_root = locate_config(Path(getcwd()), "xpider.toml", file=False)
    if project_root:
        project_file = project_root / "xpider.toml"
        with open(project_file) as project_object:
            project = tomlkit.load(project_object)
        project_name = project["xpider"]["project"]["name"]
        settings = dict(project["xpider"]["settings"])
        path.insert(0, str(project_root / "src"))
        spider_module = import_module(f"{project_name}.main")
        del path[0]
        spider_class = spider_module.Spider
        process_loop = ProcessLoop(spider_class, settings)
        process_loop.start()
