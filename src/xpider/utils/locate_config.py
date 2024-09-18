def locate_config(current_location, filename, project_root=None, file=True):
    file_location = current_location.joinpath(filename)
    if file_location.exists():
        return file_location if file else current_location
    else:
        if (
            current_location == current_location.parent
            or current_location == project_root
        ):
            return None
        else:
            return locate_config(current_location.parent, filename, file=file)
