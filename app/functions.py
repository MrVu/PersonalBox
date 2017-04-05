import os, time, string, random
from flask_login import current_user
from scandir import walk, scandir


def Installed(key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    return os.path.exists(REPO)


def Install(key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    os.makedirs(REPO)


def RandomID(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def ReadPath(path, key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    REQUESTED_PATH = os.path.join(REPO, path)

    if not os.path.exists(REQUESTED_PATH):
        return None

    try:
        stuff = next(walk(REQUESTED_PATH))
        folders = stuff[1]
        files = stuff[2]
        folders.sort()
        files.sort()
        return folders, files
    except StopIteration:
        return 0


def IsFile(path, key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    FINAL_PATH = os.path.join(REPO, path)

    if os.path.isdir(FINAL_PATH):
        return False
    else:
        return True


def RepoPath(path, key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    FINAL_PATH = os.path.join(REPO, path)

    return FINAL_PATH


def GetBasePath(key_folder):
    """Get users dir"""
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    return REPO


def MkNewDir(name, path, key_folder):
    """Create a new dir"""
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    CURRENT_PATH = os.path.join(REPO, path)
    NEW_DIR = os.path.join(CURRENT_PATH, name)
    try:
        os.makedirs(NEW_DIR)
    except OSError:
        print "ERROR OS"


def parent(path, key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    CURRENT_PATH = os.path.join(REPO, path)
    PARENT = os.path.dirname(CURRENT_PATH)
    return PARENT


def geturlpath(path, key_folder):
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO = os.path.join(LOCAL_PATH, key_folder)
    BASE_PATH = os.path.join(LOCAL_PATH, REPO)
    _len = len(BASE_PATH) + 1
    URL_PATH = path[_len:]
    return URL_PATH



def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'rar', 'zip', 'iso', 'apk'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def osWalkJson(folders, files):
    """Return a dictionary of files and folder {1:file_name}"""
    foldersjson = {}
    filesjson = {}
    for i in range(0, len(folders)):
        foldersjson[i] = folders[i]
    for i in range(0, len(files)):
        filesjson[i] = files[i]
    return foldersjson, filesjson


def getParentUrl(path, key_folder):
    current_path = os.path.join(GetBasePath(key_folder), path)
    parent_path = parent(current_path, key_folder)
    parent_url = geturlpath(parent_path, key_folder)
    return parent_url


def getDirectLink(key_folder, parent_url, file_name):
    if parent_url:
        return key_folder + '/' + parent_url + '/' + file_name
    return key_folder + '/' + file_name

def getDownloadPath(path):
    local_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(local_path,path)


def RemoveHiddenObjects(_list):
    _list2 = list()  # List that contains only visible,
    # non-hidden objects.
    for element in _list:
        if element[0] != ".":
            _list2.append(element)

    return _list2


def log(message, file="log.txt"):
    """A barebones function that logs messages."""
    line = "[{} >>> {}]\n\t{}\n\n".format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), message)
    file = open(file, "a")
    file.write(line)
    file.close()
