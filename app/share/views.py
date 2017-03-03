from . import share
from flask import render_template, send_from_directory, send_file, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from app import functions, db
from app.classmaker import classmaker
import os
from itsdangerous import URLSafeSerializer
from app.models import Shared, User


@share.route('/shared')
@login_required
def shared():
    files_dict = {}
    files = Shared.query.filter_by(user=current_user._get_current_object()).all()
    for i in range(0, len(files)):
        files_dict[i] = files[i]
    return render_template('shared.html', files_dict=files_dict, files=files,
                           classmaker=classmaker)


@share.route('/shared/<string:token>')
def token_unload(token):
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    try:
        file_url = serializer.loads(token)
        file_path = functions.getDownloadPath(file_url)
        return send_file(file_path, as_attachment=True)
    except:
        abort(404)


@share.route('/shared/remove/<string:file_id>')
def remove_shared_file(file_id):
    try:
        shared_file = Shared.query.get(file_id)
        db.session.delete(shared_file)
        db.session.commit()
        return redirect(url_for('share.shared'))
    except:
        return redirect(url_for('share.shared'))
