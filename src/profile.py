#!/use/bin/python3

from flask import Blueprint
from flask import g
from flask import render_template
from flask import request

from src.auth import login_required

from src.connectivity import get_user_by_id
from src.connectivity import check_password
from src.connectivity import update_password



bp = Blueprint ('profile', __name__)

@bp.route('/profile/', args=(page='overview'), methods=['GET', 'POST'])
@bp.route('/profile/<str:page>/', methods=['GET', 'POST'])
@login_required
def profile(page):
	user = get_user_by_id(g.user.get_uid())
	data = request.form.to_dict()
	
	if page == 'updateName':
		msgS, msgF = updateName(g.user.get_uid(), data['fn'], data['ln'])
	elif page == 'updateAddress':
		msgS, msgF = updateAddress(g.user.get_uid(), data['address'])
	elif page == 'updateMobile':
		msgS, msgF = updateMobile(g.user.get_uid(), data['mobile'])
	elif page == 'updateEmail':
		msgS, msgF = updateEmail(g.user.get_uid(), data['email'])
	elif page == 'updateSecQA':
		msgS, msgF = updateSecQA(g.user.get_uid(), data['secq'], data['seca'])
	elif page == 'updatePassword':
		msgS, msgF = updatePassword(data['oldpass'], data['pass'], data['conf'])
	else:
		msgS = msgF = ''
	
	return render_template('profile.html', name=g.user.get_username(), role=g.user.get_role(), type=page, profile=user, msgSuccess=msgS, msgFail=msgF)

def updateName():
	pass

def updateAddress():
	pass

def updateMobile():
	pass

def updateEmail():
	pass

def updateSecQA():
	pass

def updatePassword(oldpass, pass1, pass2):
	if check_password(g.user.get_username(), oldpass):
		if pass1 == pass2:
			update_password(g.user.get_username())
			return 'Password Updated Successfully', ''
		return '', 'Passwords do not match'
	return '', 'Enter correct Password'


