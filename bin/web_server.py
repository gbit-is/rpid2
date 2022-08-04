from flask import Flask,request
from init import *
kvs = init_kvs() # initalise KVS, make sure the KVS is populated 



app = Flask(__name__)



@app.route('/')
def hello_world():
	return 'Hello World'


@app.route("/config/<parameter>", methods = ['POST','GET'])
def manageConfig(parameter):
	kvs = init_kvs()

	keys = [ ]	
	for key in kvs.keys():
		keys.append(key.decode())

	if parameter not in keys:
		return "parameter not in KVS",404


	if request.method == 'POST':
		data = request.data.decode()
		if len(data) == 0:
			return "body recieved is empty",400
		else:
			try:
				kvs[parameter] = data
				return "ack", 200
			except Exception as e:
				return e, 500
		
		
	elif request.method == 'GET':
		data = kvs[parameter].decode()
		return data



 


 
if __name__ == '__main__':
 
	app.run(host="0.0.0.0")
	pass


