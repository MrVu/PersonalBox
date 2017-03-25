from flask import render_template, session, redirect, url_for, send_from_directory, request, jsonify, abort, \
    current_app, flash
from itsdangerous import URLSafeSerializer
from werkzeug.utils import secure_filename
from . import main
from .. import db
from app import functions
from .forms import NewFolder, FileUpload
import os, shutil
from flask_login import login_required, current_user
from app.files import *
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
        file_list = request.files.getlist('files')
        for file in file_list:
            file_length = request.content_length
            if not check_storage_limit(current_user, file_length):
                flash('Sorry you out of your storage, please upgrade account')
                response = {'status': 0}
                return jsonify(response)
            if file and functions.allowed_file(file.filename):
                current_path = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
                file_name = secure_filename(file.filename)
                try:
                    file.save(os.path.join(current_path, file_name))
                    update_used_storage(current_user, file_length)
                    response = {'status': 1}
                except Exception as e:
                    current_app.logger.warning(e)
                    response = {'status': 0}
            else:
                flash("Sorry, your file extension is not allowed at Ubox")
                response = {'status': 0}
                current_app.logger.warning("Some one upload wrong extention: " + current_user.email + ':' + file.filename)
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
    current_path = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
    parent_local_path = functions.parent(current_path, key_folder)
    parent_url = functions.geturlpath(parent_local_path, key_folder)
    if request.method == 'POST' and 'files' in request.files:
        file_list = request.files.getlist('files')
        for file in file_list:
            file_length = request.content_length
            if not check_storage_limit(current_user, file_length):
                flash('Sorry you out of your storage, please upgrade account')
                response = {'status': 0}
                return jsonify(response)
            if file and functions.allowed_file(file.filename):
                current_path = os.path.join(functions.GetBasePath(key_folder), BASE_PATH)
                file_name = secure_filename(file.filename)
                try:
                    file.save(os.path.join(current_path, file_name))
                    update_used_storage(current_user, file_length)
                    response = {'status': 1}
                except Exception as e:
                    current_app.logger.warning(e)
                    response = {'status': 0}
            else:
                flash("Sorry, your file extension is not allowed at Ubox")
                response = {'status': 0}
                current_app.logger.warning("Some one upload wrong extention: " + current_user.email + ':' + file.filename)
        return jsonify(response)

    elif form.validate_on_submit():
        new_folder = form.folder.data
        functions.MkNewDir(new_folder, path, key_folder)
        return redirect(url_for('main.browse', path=path))

    if functions.ReadPath(path, key_folder) is None:
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
    except Exception as e:
        current_app.logger.error(e)
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
        current_app.logger.error(e)
        return redirect(url_for('share.shared'))
    return redirect(url_for('share.shared'))


@main.route('/remove/<path:path>')
@login_required
def remove(path):
    key_folder = current_user.userkey
    current_path = os.path.join(functions.GetBasePath(key_folder), path)
    parent_url = functions.getParentUrl(path, key_folder)
    try:
        if functions.IsFile(path, key_folder):
            file_size = get_file_size(current_path)
            os.remove(current_path)
            minus_file_size(current_user, file_size)
        else:
            folder_size = get_folder_size(current_path)
            shutil.rmtree(current_path)
            minus_file_size(current_user, folder_size)
        return redirect(url_for('main.browse', path=parent_url))
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
