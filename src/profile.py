#!/use/bin/python3

from flask import Blueprint

from src.auth import login_required


bp = Blueprint ('profile', __name__)

@bp.route('/profile/', args=(page='overview'), methods=['GET', 'POST'])
@bp.route('/profile/<str:page>/', methods=['GET', 'POST'])
@login_required
def profile(page):
