from flask import Blueprint, request, render_template, send_from_directory
import os

from app.myglobals import logfolder

#
blue_log = Blueprint('blue_log', __name__, url_prefix='/log')


@blue_log.route('/')
def log():
    filelist = os.listdir(logfolder)
    return render_template('log.html', filelist=filelist)

@blue_log.route('/view/')
def cmd_logview():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=False)

@blue_log.route('/download/')
def cmd_logdownload():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=True)

