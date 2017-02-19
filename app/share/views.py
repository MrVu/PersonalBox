from . import share
from flask import render_template, send_from_directory, send_file, redirect, url_for
from flask_login import login_required, current_user
from app import functions
from app.classmaker import classmaker
import os


@share.route('/shared')
@login_required
def shared():
    key_folder = current_user.userkey
    folders, files = functions.sharedWalk(key_folder)
    return render_template('shared.html', key_folder=key_folder, folders=folders, files=files, classmaker=classmaker)


@share.route('/shared/<path:path>')
def sharedFileDownload(path):
    shared_file = functions.getSharedFile(path)
    return send_file(shared_file, as_attachment=True)

@share.route('/shared/remove/<path:path>')
def remove_shared_file(path):
    key_folder= current_user.userkey
    folder= functions.getUserSharedPath(key_folder)
    f= os.path.join(folder,path)
    try:
        os.remove(f)
        return redirect(url_for('share.shared'))
    except:
        return redirect(url_for('share.shared'))
