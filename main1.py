from flask import Flask,redirect,url_for,render_template,request,flash
from flask_login import LoginManager,current_user,login_user,logout_user,login_required
from flask_mail import Mail,Message
from random import randint
from db import Register,Base,User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app=Flask(__name__)
app.secret_key='ss'

engine=create_engine('sqlite:///LIST.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

@app.route('/p')
def d():
	return "Welcomeee!!!"

@app.route("/index")
def index():
	return render_template('index1.html')

@app.route('/show')
#@login_required
def showData():
	register1=session.query(Register).all()
	return render_template('show.html',reg=register1)

@app.route('/add',methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			email=request.form['email'],
			password=request.form['pass'])
		session.add(newData)
		session.commit()
		flash("New data is added")
		return redirect(url_for('showData'))
	else:
		return render_template('add.html')

@app.route('/edit/<int:register_id>',methods=['POST','GET'])
def editData(register_id):
	editeddata=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editeddata.name=request.form['name']
		editeddata.email=request.form['email']
		editeddata.password=request.form['pass']
		session.add(editeddata)
		session.commit()
		flash("data is edited")

		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editeddata)

@app.route('/delete/<int:register_id>',methods=['POST','GET'])
def deleteData(register_id):
	deletedata=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deletedata)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('delete.html',register=deletedata)

@app.route('/register',methods=['POST','GET'])
def registerData():
	if request.method=='POST':
		regdata=User(name=request.form['name'],email=request.form['email'],password=request.form['password'])
		session.add(regdata)
		session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('register.html')

@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('showData'))
	try:
		if request.method=='POST':
			user=session.query(User).filter_by(
				email=request.form['email'],
				password=request.form['password']).first()
			if user:
				login_user(user)
				return redirect(url_for('showData'))
			else:
				flash('Login Failed')
		else:
			return render_template('login.html')
	except Exception as e:
		flash("Login failed")
	else:
		return render_template('login.html')
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index')) 

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))



'''

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='ganiraju100@gmail.com'
app.config['MAIL_PASSWORD']='*******'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


mail=Mail(app)
otp=randint(000000,999999)
app.secret_key='gg'

@app.route('/email')
def email():
	return render_template('email.html')
@app.route('/email_verify',methods=['POST','GET'])
def email_verify():
	email=request.form['mail']
	msg=Message('OTP for verification',sender='ganiraju100@gmail.com',recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template('email_verify.html')
@app.route('/validation',methods=['POST','GET'])
def validation():
	user_otp=request.form['otpvalue']
	if otp==int(user_otp):
		return "OTP verification is done"
	else:
		return "Invalid OTP"





@app.route('/home/<name>')
def index(name):
	return "<h1> Good Evening Gani </h1>" +name
@app.route('/index/<int:age>')
def index1(age):
	return "<h1> RamaniGani </h1>  {}" .format(age)

@app.route('/user/<float:age>')
def index2(age):
	return " %f" %age
#function mapping
@app.route('/adminurl')
def admin():
	return "<h1> This is admin page </h1>"
@app.route('/studenturl')
def student():
	return "<h1> This is student page</h1>"
@app.route('/user/<name>')
def home(name):
	if name=='adimin':
		return redirect(url_for('admin'))
	if name=='student':
		return redirect(url_for('student'))
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/loginpage/<name>')
def loginpage(name):
	return render_template('login page.html',username=name)
@app.route('/table/<int:value>')
def table(value):
	return render_template('table.html',n=value)
	 
@app.route('/upload')
def upload():
	return render_template('upload.html')
@app.route('/success',methods=['POST','GET'])
def success():
	if request.method=="POST":
		f=request.files['image']
		f.save(f.filename)
		return render_template('success.html',name=f.filename)
	else:
		return "Please check code" '''
if __name__=='__main__':
	app.run(debug=True)