from flask import Blueprint, g, render_template
from werkzeug.security import check_password_hash, generate_password_hash

# A Blueprint is a way to organize a group of related views and other code.
bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/main')
def main():
    user = 'hello'
    return render_template("base.html", user=user)
