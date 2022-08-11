from flask import Flask,request,render_template
from init import *
config = init_config()
kvs = init_kvs() # initalise KVS, make sure the KVS is populated 


def validateKvsValue(key,value):

	if key in config["kvs_variables"]:
		valueType = config["kvs_variables"][key]
			
		if valueType == "bool":
			if value in [ "True","False" ]:
				return True
			else:
				return False


		elif valueType == "num":
			try:
				value = float(value)
				return True
			except:
				return False
			
	else:
		return True


app = Flask(__name__)


app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def hello_world():

	kvs = init_kvs() 

	audioLoopEnabled = kvs["audio_loop_enabled"].decode()

	if audioLoopEnabled == "True":
		audioChecked_var = "checked"
	else:
		audioChecked_var = ""

	return render_template('index.html', audioChecked=audioChecked_var)



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
			
			valid = validateKvsValue(parameter,data)
			
			if valid:

				try:
					kvs[parameter] = data
					return "ack", 200
				except Exception as e:
					return e, 500
			else:
				return "unable to validate k:v pair", 418
		
		
	elif request.method == 'GET':
		data = kvs[parameter].decode()
		return data



 


 
if __name__ == '__main__':
 
	app.run(host="0.0.0.0")
	pass


