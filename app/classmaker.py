def classmaker(filename):
    length = len(filename)
    extension = filename[(length-3):]
    extension2 = filename[(length-2):]
    extension4 = filename[(length-4):]
    if extension == "png" or extension== "jpg":
        file_class= "glyphicon glyphicon-picture"
    elif extension== "pdf" or extension == "doc" or extension== "txt":
        file_class= "glyphicon glyphicon-list-alt"
    elif extension == "mp4":
        file_class = "glyphicon glyphicon-film"
    elif extension == "mp3":
        file_class = "glyphicon glyphicon-music"
    else:
        file_class= "glyphicon glyphicon-file"
    return file_class