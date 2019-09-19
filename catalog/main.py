from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker#database to database connection
from sqlalchemy import create_engine#to add data form form and to store

engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
engine=create_engine('sqlite:///use.db')
engine=create_engine('sqlite:///use.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine#data ni combine chesi store chesukuntundhi binded to engine
DBsession=sessionmaker(bind=engine)
session=DBsession()#to store ,retrive,display

app=Flask(__name__) #name defines project

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='santhimedagam@gmail.com'
app.config['MAIL_PASSWORD']='msanthip'
app.config['MAIL_USE-TLS']=False
app.config['MAIL_USE_SSL']=True
app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")
def demo():
	return "Hello world welcome to apssdc"

@app.route("/sample1")
def demo1():
	return "<h1>Hello Demo page</h1>"
@app.route("/info/details")
def demo2():
	return "hello details"

@app.route("/details/<name>")
def demo3(name):
	return "hello {}".format(name)
@app.route("/inf/<name>/<int:age>/<float:salary>")
def demo4(name,age,salary):
	return " Hello name is {} and age is {} and salary is {}".format(name,age,salary)


#url_for example(redirecting to the url)
@app.route("/admin")
def admin():
	return "Hello Admin"
@app.route("/student")
def student():
	return "Hello Student"
@app.route("/staff")
def staff():
	return "Hello Staff"

@app.route("/info/<name>")
def admin_info(name):
	if name=='admin':
		return redirect(url_for('staff'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='staff':
		return redirect(url_for('admin'))

	else:
		return "No URL"

@app.route("/data")
def demo_html():
	return render_template('sample.html')
@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html1(name,age,sal):
	return render_template('sample.html',n=name,a=age,s=sal)
@app.route("/sam")
def demo_html2():
	sno=20
	name="santhi"
	branch="E2"
	dept="CSE"
	return render_template('sample1.html',s_no=sno,n=name,b=branch,d=dept)


adata=[{'s_no':123,'name':'santhi','branch':'IT','dept':'CSE'},
{'s_no':113,'name':'sam','branch':'EC','dept':'ECE'}]
@app.route("/dummy_data")
def dummy():
		return render_template('sample1.html',dummy_data=data)
#table printing
app.route("/table/<int:number>")
def table1(number):
	return render_template('data.html',n=number)

#file uploading
@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
	return render_template("file_upload.html")
@app.route("/success",methods=['GET','POST'])
def success():
	if request.method=='POST':
		f=request.files['file']
		f.save(f.filename)

		return render_template('success.html',f_name=f.filename)
#mail sending
@app.route("/email")
def email_send():
	return render_template('email.html')

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
	email=request.form['email'] 
	msg=Message("One Time Password",sender="santhimedagam@gmail.com",recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template('v_email.html')
@app.route("/email_success",methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "Invalid OTP"

#to dispaly contents of the database
@app.route("/show")
def showData():
	register=session.query(Register).all()

	return render_template('show.html',reg=register)


@app.route("/login")
def loginpage():
	return render_template('login.html')
@app.route("/registeruser")
def registeruser():
	return render_template('register.html')

@app.route("/new",methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],surname=request.form['surname'],
			mobile=request.form['mobile'],email=request.form['email'],
			branch=request.form['branch'],role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("Data added successfully")
		return redirect(url_for('showData'))
	else:
		return render_template('new.html')	
@app.route("/")
def Navigation():
	return render_template("navigation.html")

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.mobile=request.form['mobile']
		editedData.email=request.form['email']
		editedData.branch=request.form['branch']
		editedData.role=request.form['role']
		session.add(editedData)
		session.commit()
		flash("Data edited successfully")
		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)
@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		deletedData.name=request.form['name']
		session.delete(deletedData)
		session.commit()
		flash("Data deleted successfully {}".format(deletedData.name))
		return redirect(url_for('showData'))
	else:
		return render_template('delete.html',register=deletedData)
@app.route("/show_user")
def userData():
	register=session.query(User).all()

	return render_template('use.html',use=register)


	



if __name__=='__main__': #to run automatically server
	app.run(debug=True)#if we won't turn on debug we have to modify every time

