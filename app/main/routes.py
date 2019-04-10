from flask import render_template
from flask_login import current_user, login_required
from app.main import bp


@bp.route('/')
@login_required
def index():
    return render_template('main/index.html', headline='Hello, {}'.format(current_user.username))


@bp.route('/current_lib')
def user_library():
    pass
