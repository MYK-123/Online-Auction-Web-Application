#!/use/bin/python3

from flask import Blueprint
from flask import g
from flask import render_template
from flask import request

from src.auth import login_required

from src.connectivity import get_user_by_id
from src.connectivity import check_password
from src.connectivity import update_password

from src.connectivity.db import update_email
from src.connectivity.db import update_mobile
from src.connectivity.db import update_address
from src.connectivity.db import update_secqa
from src.connectivity.db import update_name



bp = Blueprint ('profile', __name__)

@bp.route('/profile/', methods=['GET', 'POST'])
@bp.route('/profile/<string:page>/', methods=['GET', 'POST'])
@login_required
def profile(page='overview'):
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

def updateName(uid, fn, ln):
	update_name(uid, fn, ln)
	return 'Name Updated Successfully', ''

def updateAddress(uid, address):
	update_address(uid, address)
	return 'Address Updated Successfuy', ''

def updateMobile(uid, mobile):
	update_mobile(uid, mobile)
	return 'Mobile Updated Sucessfully', ''

def updateEmail(uid, email):
	update_email(uid, email)
	return 'Email Updated Successfully', ''

def updateSecQA(uid, q, a):
	update_secqa(uid, q, a)
	return 'Security Question/Answer Updated Successfully', ''

def updatePassword(oldpass, pass1, pass2):
	if check_password(g.user.get_username(), oldpass):
		if pass1 == pass2:
			update_password(g.user.get_username())
			return 'Password Updated Successfully', ''
		return '', 'Passwords do not match'
	return '', 'Enter correct Password'


