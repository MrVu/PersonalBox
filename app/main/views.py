from flask import render_template, session, redirect, url_for, send_from_directory, request, jsonify
from . import main
from .. import db
from app import functions
from .forms import NewFolder, FileUpload
import os, shutil
from flask_login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('main.root'))


@main.route('/browse', methods=['GET', 'POST'])
@main.route('/browse/', methods=['GET', 'POST'])
@login_required
def root():
    key_folder = current_user.userkey
    BASE_PATH = ""
    form = NewFolder()
    upload_form = FileUpload()

    if request.method == 'POST' and 'files' in request.files:
        file= request.files['files']
        CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
        try:
            file.save(os.path.join(CURRENT_PATH, file.filename))
            response= {'status': 1}
        except:
            response={'status': 0}
        return jsonify(response)
    elif form.validate_on_submit():
        new_folder = form.folder.data
        functions.MkNewDir(new_folder, BASE_PATH, key_folder)
        return redirect(url_for('main.root'))

    folders, files = functions.ReadPath("", key_folder)
    return render_template('root.html', form=form, upload_form=upload_form, folders=folders, files=files,
                           BASE_PATH=BASE_PATH)


@main.route('/browse/<path:path>', methods=['GET', 'POST'])
@login_required
def browse(path):
    key_folder = current_user.userkey
    BASE_PATH = path
    form = NewFolder()
    upload_form = FileUpload()
    # if upload_form.validate_on_submit():
    # file_data = upload_form.upload_file.data
    # CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
    # file_data.save(os.path.join(CURRENT_PATH, file_data.filename))
    # return redirect(url_for('main.browse', path=path))
    if request.method == 'POST' and 'files' in request.files:
        file = request.files['files']
        CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
        try:
            file.save(os.path.join(CURRENT_PATH, file.filename))
            response = {'status': 1}
        except:
            response = {'status': 0}
        return jsonify(response)
    elif form.validate_on_submit():
        new_folder = form.folder.data
        functions.MkNewDir(new_folder, path, key_folder)
        return redirect(url_for('main.browse', path=path))

    if functions.ReadPath(path, key_folder) == None:
        Error404 = True
        return render_template('browse.html', Error404=Error404, form=form, upload_form=upload_form)

    elif functions.IsFile(path, key_folder):
        return send_from_directory(functions.GetBasePath(key_folder), path)

    else:
        folders, files = functions.ReadPath(path, key_folder)
        return render_template('browse.html', upload_form=upload_form, form=form, folders=folders, files=files,
                               BASE_PATH=BASE_PATH)


@main.route('/download/<path:path>')
@login_required
def download(path):
    key_folder = current_user.userkey
    return send_from_directory(functions.GetBasePath(key_folder), path, as_attachment=True)


@main.route('/remove/<path:path>')
@login_required
def remove(path):
    key_folder = current_user.userkey
    CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), path)
    PARENT = functions.parent(CURRENT_PATH, key_folder)
    PARENT_URL = functions.geturlpath(PARENT, key_folder)
    if functions.IsFile(path, key_folder):
        os.remove(CURRENT_PATH)
    else:
        shutil.rmtree(CURRENT_PATH)
    return redirect(url_for('main.browse', path=PARENT_URL))