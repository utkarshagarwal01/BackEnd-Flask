from app import app
from flask import jsonify, request

import json

import sqlite3

password = "TOP_SECRET"

def dataFormatter(code,message,data):
	resp = jsonify({
			'code':code,
			'message':message,
			'data':data
		})
	resp.status_code=code
	return resp

@app.route('/student',methods=['GET','POST'])
def getStudents():
	if request.method == 'GET':
		try:
			conn = sqlite3.connect('data/univ.db')
			try:
				qname = request.args.get('name') 
				cursor = conn.execute("SELECT * FROM Student WHERE name = (?) ORDER BY ID",(qname,))
			except:
				cursor = conn.execute("SELECT * FROM Student ORDER BY ID")

			students = []
			#cursor = conn.execute("SELECT * FROM Student ORDER BY ID")
			for row in cursor:
				stud={}
				stud['ID']=row[0];
				stud['name']=row[1];
				stud['dept_name']=row[2];
				stud['tot_cred']=row[3];
				students.append(stud)

			message = "Success. Found "+str(len(students))+" students."

			return dataFormatter(200,message,students)
		except:
			return dataFormatter(404,"Not Found!",[])
		finally:
			conn.close()
	elif request.method == 'POST':
		
		try:
			sentpass = request.headers.get('Authorization')
			if(sentpass != password):
				return dataFormatter(401,"Unauthorized.",[])
		except:
			return dataFormatter(400,"Bad Request. Specify Header",[])


		try:
			conn = sqlite3.connect('data/univ.db')
			try:
				qid = request.form.get("ID")
				qname = request.form.get("name")
				qdeptname = request.form.get("dept_name")
				qtotCred = request.form.get("tot_cred")
				
				cursor = conn.execute("SELECT * FROM Student WHERE ID = (?)",(qid,))
			
				studs = []
			#cursor = conn.execute("SELECT * FROM Student ORDER BY ID")
				for row in cursor:
					studs.append(row[0])
				if len(studs) > 0:
					return dataFormatter(409,"Already Present",[])

				try:
					cursor = conn.execute("INSERT into student(ID,name,dept_name,tot_cred) VALUES (?,?,?,?)",(qid,qname,qdeptname,qtotCred,))
					conn.commit() #push to database
					return dataFormatter(200,"Inserted Successfully",[])
				except:
					return dataFormatter(500,"Internal Server Error.",[])
			except:
				return dataFormatter(400,"Unauthorized. Need fields.",[])
		except:
			return dataFormatter(404,"Unable to connect.",[])
		finally:
				conn.close()

# with open('data/people.json') as data_file:
# 	data=json.load(data_file)

# #update the json file
# def saveFile():
# 	with open('data/people.json') as outfile:
# 		json.dump(data.outfile)

# # @app.route('/',methods=['GET'])
# # def mainRoute():
# # 	l= ["SOME","Data","Here"]
# # 	return dataFormatter(201,"Success",l)


# @app.route('/number/<num>',methods=['GET'])
# def square(num):
# 	try:
# 		sq=int(num)*int(num)
# 		ret = "Square of "+ num + " is " + str(sq)
# 		return dataFormatter(200,"Sucsess.",ret)
# 	except:
# 		ret = "Error: Pass a number"
# 		return dataFormatter(400,"Fail",ret)

# @app.route('/', methods=['GET'])
# def personList():
#  	return dataFormatter(201,"Success",data)

# @app.route('/favs',methods=['GET'])
# def favs_list():
# 	l = []
# 	for person in data:
# 		if (person["isFav"] == True):
# 			l.append(person) 

# 	return dataFormatter(201,"Success",l)

# @app.route('/add',methods = ['POST'])
# def addPerson():
# 	name = request.form.get('name','')
# 	location = request.form.get('location','')
# 	status = request.form.get('status','')
# 	new_person = {
# 			'name':name,
# 			'location':location,
# 			'status':status,
# 			'isFav':False,
# 			'isNew':True
# 			}
# 	data.append(new_person)
# 	return dataFormatter(201,"Successfully added",data)


# # @app.route('/',methods=['GET'])
# # def mainRoute():
# # 	return "Hello World!"

# # @app.route('/number/<num>',methods=['GET'])
# # def square(num):
# # 	try:
# # 		sq=int(num)*int(num)
# # 		return str("Square of "+ num + " is " + str(sq));
# # 	except:
# # 		return "Pass a number!"

# # @app.route('/string/<string>', methods=['GET','POST'])
# # def string(string):
# # 	# GET
# # 	if(request.method == 'GET'):
# # 		return "You're GETting it, " + string + "!"
# # 	# POST
# # 	elif(request.method == 'POST'):
# # 		return "You're POSTing it, " + string.upper() + "!"