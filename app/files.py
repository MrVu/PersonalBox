from app import db
import os
from scandir import scandir, walk


def classmaker(filename):
    length = len(filename)
    extension = filename[(length - 3):]
    extension2 = filename[(length - 2):]
    extension4 = filename[(length - 4):]
    if extension.lower() == "png" or extension.lower() == "jpg":
        file_class = "glyphicon glyphicon-picture"
    elif extension.lower() == "pdf" or extension == "doc" or extension == "txt":
        file_class = "glyphicon glyphicon-list-alt"
    elif extension.lower() == "mp4":
        file_class = "glyphicon glyphicon-film"
    elif extension.lower() == "mp3":
        file_class = "glyphicon glyphicon-music"
    else:
        file_class = "glyphicon glyphicon-file"
    return file_class


def check_storage_limit(user, file_length):
    storage = user.storage
    storage_used = user.storage_used
    if file_length + storage_used > storage:
        return False
    return True


def used_storage_percent(storage, used):
    return used / storage


def update_used_storage(user, file_length):
    try:
        current_used_storage = user.storage_used
        updated_used_storage = current_used_storage + file_length
        user.storage_used = updated_used_storage
        db.session.add(user)
        db.session.commit()
    except Exception as Error:
        return Error


def get_file_size(path):
    return os.path.getsize(path)


def minus_file_size(user, file_size):
    used_storage = user.storage_used
    current_used_storage = used_storage - file_size
    user.storage_used = current_used_storage
    db.session.add(user)
    db.session.commit()


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

