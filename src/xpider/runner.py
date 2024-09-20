from importlib import import_module
from os import getcwd
from pathlib import Path
from sys import path
from xpider.utils.locate_config import locate_config
import tomlkit
from xpider.processor.process_loop import ProcessLoop
from os import environ
from typing import Optional

def update_settings(settings:dict,project_name:str, cmd_args:Optional[dict]=None):
    mongo_url = cmd_args.get("mongo_url", None) if cmd_args is not None  else None
    redis_url = cmd_args.get("redis_url", None) if cmd_args is not None  else None
    mongo_url = environ.get("XPIDER_MONGO_URL") if mongo_url is None else mongo_url
    redis_url = environ.get("XPIDER_REDIS_URL") if redis_url is None else redis_url
    settings["mongo_url"] = mongo_url
    settings["redis_url"] = redis_url
    settings["name"] = project_name





def runner(cmd_args:Optional[dict]=None):
    cmd_args = cmd_args if cmd_args is not None else {}
    project_root =  cmd_args.get("path")
    project_root = Path(project_root) if project_root is not None else locate_config(Path(getcwd()), "xpider.toml", file=False)
    if project_root:
        project_file = project_root / "xpider.toml"
        with open(project_file) as project_object:
            project = tomlkit.load(project_object)
            project = dict(project)
        project_name = project["xpider"]["project"]["name"]
        settings = dict(project["xpider"]["settings"])
        update_settings(settings, project_name, cmd_args)
        path.insert(0, str(project_root / "src"))
        spider_module = import_module(f"{project_name}.main")
        del path[0]
        spider_class = spider_module.Spider
        process_loop = ProcessLoop(spider_class, settings)
        process_loop.start()
