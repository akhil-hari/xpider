from os import getcwd
from pathlib import Path
from xpider.utils.name_tools import snake_case
from tomlkit import document, dump


def generate_project(name: str):
    project_name = snake_case(name)
    current_path = Path(getcwd())
    project_path = current_path / project_name
    code_path = project_path / f"src/{project_name}"
    try:
        (code_path/"items").mkdir(parents=True)

    except Exception as error:
        print(error)
        exit()
    keys = ["description", "repo", "author", "email", "website"]
    raw_project_dict = {"name": project_name}
    for key in keys:
        raw_project_dict[key] = input(f"{key}:\t")
    repo = raw_project_dict.get("repo", "")
    author = raw_project_dict.get("author", "")
    email = raw_project_dict.get("email", "")
    website = raw_project_dict.get("website", "")
    description = raw_project_dict.get("description", "")
    project_dict = {
        "name": project_name,
        "description": description,
        "repo": repo,
        "author": author,
        "email": email,
        "website": website,
    }
    doc = document()
    xpider_doc = document()
    xpider_doc["project"] = project_dict
    xpider_doc["settings"] = {
        "threads": 5,
        "max_retry": 20,
        "timeout": 20,
    }
    doc["xpider"] = xpider_doc
    dump(doc, (project_path / "xpider.toml").open("w"))
    authors = [f"{author} <{email}>"] if author and email else []
    pyproject_dict = {
        "tool": {
            "poetry": {
                "name": name,
                "version": "0.0.1",
                "description": description,
                "authors": authors,
                "license": "none",
                "packages": [{"include":name, "from":"src"}],
                "dependencies": {
                    "python": ">=3.11,<4.0",
                    "xpider": "*",
                    "lxml": "*",
                },
                "dev-dependencies": {},
            }
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        },
    }
    doc = document()
    doc["tool"] = pyproject_dict["tool"]
    doc["build-system"] = pyproject_dict["build-system"]
    dump(doc, (project_path / "pyproject.toml").open("w"))
    poetry_dict = {"virtualenvs": {"in-project": True}}
    dump(poetry_dict, (project_path / "poetry.toml").open("w"))
    generate_python_files(code_path, project_name)

def generate_python_files(code_path:Path, name:str):
    page_py = code_path / "items/page.py"
    main_py = code_path / "main.py"
    
    template_base = Path(__file__).parent / "python_file_template"
    
    page_py.open("w").write((template_base / "page").open().read())
    main_py.open("w").write((template_base / "main").open().read().format(name=name))


