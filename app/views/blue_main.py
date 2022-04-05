from flask import Blueprint, request, render_template

blue_main = Blueprint('blue_main', __name__)

@blue_main.route('/')
@blue_main.route('/index/')
def vf_index():
    return render_template('main_index.html')
