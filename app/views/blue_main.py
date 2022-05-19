from flask import Blueprint, request, render_template, send_from_directory
import os

from app.myglobals import staticfolder

blue_main = Blueprint('blue_main', __name__)

@blue_main.route('/')
@blue_main.route('/index/')
def index():
    return render_template('main_index.html')

@blue_main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(staticfolder, 'pic'),
                               'cbyge.png', mimetype='image/vnd.microsoft.icon')
