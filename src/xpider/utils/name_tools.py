import re


def snake_case(name):
    name = name.strip(" _")
    name = name.lower()
    name = name.replace(" ", "_")
    return name


def pascal_case(name):
    name = name.strip(" _")
    name = name.title()
    name = name.replace(" ", "")
    name = name.replace("_", "")
    return name


def camel_case(name: str) -> str:
    name = pascal_case(name)
    name = name[0].lower() + name[1:]
    return name


def train_case(name):
    name = re.sub("([A-Z])", r"-\1", name)
    name = name.replace(" ", "-")
    name = name.replace("_", "-")
    name = name.lower()
    name = name.strip(" _-")
    return name
