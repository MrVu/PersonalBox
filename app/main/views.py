from flask import render_template, session, redirect, url_for, send_from_directory, request, jsonify, abort, current_app
from itsdangerous import URLSafeSerializer
from werkzeug.utils import secure_filename
from . import main
from .. import db
from app import functions
from .forms import NewFolder, FileUpload
import os, shutil
from flask_login import login_required, current_user
from app.classmaker import classmaker
from app.models import User, Shared


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
        file = request.files['files']
        if file and functions.allowed_file(file.filename):
            CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
            file_name = secure_filename(file.filename)
            try:
                file.save(os.path.join(CURRENT_PATH, file_name))
                response = {'status': 1}
            except:
                response = {'status': 0}
            return jsonify(response)
    elif form.validate_on_submit():
        new_folder = form.folder.data
        functions.MkNewDir(new_folder, BASE_PATH, key_folder)
        return redirect(url_for('main.root'))

    folders, files = functions.ReadPath("", key_folder)
    foldersjson, filesjson = functions.osWalkJson(folders, files)
    return render_template('root.html', form=form, classmaker=classmaker, upload_form=upload_form,
                           foldersjson=foldersjson,
                           filesjson=filesjson,
                           BASE_PATH=BASE_PATH)


@main.route('/browse/<path:path>', methods=['GET', 'POST'])
@login_required
def browse(path):
    key_folder = current_user.userkey
    BASE_PATH = path
    form = NewFolder()
    upload_form = FileUpload()
    CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
    parent_local_path = functions.parent(CURRENT_PATH, key_folder)
    parent_url = functions.geturlpath(parent_local_path, key_folder)
    if request.method == 'POST' and 'files' in request.files:
        file = request.files['files']
        if file and functions.allowed_file(file.filename):
            CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
            file_name = secure_filename(file.filename)
            try:
                file.save(os.path.join(CURRENT_PATH, file_name))
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
        foldersjson, filesjson = functions.osWalkJson(folders, files)
        return render_template('browse.html', upload_form=upload_form, classmaker=classmaker, form=form,
                               foldersjson=foldersjson, filesjson=filesjson,
                               BASE_PATH=BASE_PATH, parent_url=parent_url)


@main.route('/download/<path:path>')
@login_required
def download(path):
    try:
        key_folder = current_user.userkey
        return send_from_directory(functions.GetBasePath(key_folder), path, as_attachment=True)
    except:
        abort(404)


@main.route('/send/<path:path>')
@login_required
def send_to_shared_folder(path):
    key_folder = current_user.userkey
    parent_url = functions.getParentUrl(path, key_folder)
    if parent_url and parent_url.strip():
        file_name = path[len(parent_url) + 1:]
    else:
        file_name = path[len(parent_url):]
    url = functions.getDirectLink(key_folder, parent_url, file_name)
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(url)
    direct_url = token
    try:
        share_file = Shared(file_name=file_name, file_url=direct_url, user=current_user._get_current_object())
        db.session.add(share_file)
        db.session.commit()
    except Exception as e:
        return "ERROR HAPPEN " + e
    return redirect(url_for('share.shared'))


@main.route('/remove/<path:path>')
@login_required
def remove(path):
    key_folder = current_user.userkey
    CURRENT_PATH = os.path.join(functions.GetBasePath(key_folder), path)
    parent_url = functions.getParentUrl(path, key_folder)
    try:
        if functions.IsFile(path, key_folder):
            os.remove(CURRENT_PATH)
        else:
            shutil.rmtree(CURRENT_PATH)
        return redirect(url_for('main.browse', path=parent_url))
    except:
        abort(404)
