from flask import Flask, jsonify, request, render_template, session, redirect, url_for, escape, flash
from wrappers import require_api_token
import requests
from forms import RegistrationForm
import json

base_url = 'http://13.232.122.165'

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'o5Mrqx3h9R'

# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)

# @app.route('/img/<path:path>')
# def send_js(path):
#     return send_from_directory('', path)    

@app.route('/')
def index():
	#print session
	return render_template('index.html')

@app.route('/profile')
@require_api_token
def get_profile():
	# print session['logged_in']
	r = requests.get('http://13.232.122.165/users/profile/{}'.format(session['username']))
	if r.status_code == 200:

		return render_template('profile.html')
	return redirect('/setup-profile')

@app.route('/static/images/<int:pid>.jpg')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

@app.route('/login',methods=['POST','GET'])
def login_user():
	if request.method =='POST':
		username, password = request.form.get('username'), request.form.get('password')
		r = requests.post(url = base_url+'/users/login/', data={"username":username, "password":password})
		print (r, r.text, r.cookies, r.headers, r.status_code)
		if r.status_code == 200:
			token = r.json()['auth_token']
			# # session.pop()
			session['username'] = username
			session['logged_in'] = True
			return redirect('/profile')
	return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register_user():
	form = RegistrationForm(request.form)
	#print request.form
	print (form.errors,form.validate())
	if request.method=='POST' and form.validate():
		data = { 

				'username':form.username.data,
				'email':form.email.data,
				'first_name':form.first_name.data,
				'last_name':form.last_name.data,
				'password':form.password.data,

				}
		r = requests.post(url = base_url+'/users/register/', data = data)
		#print r,r.text

		if r.status_code == 400:
			error = json.loads(r.text.decode()) 
			#print error
			return render_template('register.html', error = error)
		if r.status_code == 201:
			token = r.json()['auth_token']
			# session.pop()
			session['auth_token'] = token
			session['logged_in'] = True
			return redirect('/set-')
		pass
	return render_template('register.html')


@app.route('/setup-profile', methods=['POST','GET'])
def setup_profile():
	return render_template('setup-profile.html')
	pass

# if __name__ == '__main_':
app.run(debug=True, port=5000) 
