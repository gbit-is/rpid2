import os
import ZODB, ZODB.FileStorage
from ZODB import DB

from ZEO import ClientStorage
import transaction
from persistent import Persistent
from persistent.mapping import PersistentMapping
from collections.abc import Mapping
import configparser
import logging

logger = logger = logging.getLogger("json_db")

class MyData(Persistent):
    def __init__(self, value):
        self.value = value


class json_db():


	def __populate__(self,overwrite=False):

		def set_type(value_raw):
			value = value_raw.split(":")[0]
			value_type = value_raw.split(":")[1]
			if len(value_raw.split(":")) > 2:
				http_type = value_raw.split(":")[2]
				if len(value_raw.split(":")) > 3:
					http_extra = value_raw.split(":")[3]
				else:
					http_extra = None
			else:
				http_type = None
				http_extra = None

			if value_type == "bool":
				value = bool(value)
			elif value_type  == "str":
				value = str(value)
			elif value_type == "int":
				value = int(value)
			elif value_type == "float":
				value = float(value)
			else:
				value_type = "str"
			

			return value,value_type,http_type,http_extra
			

		def create_nested_key(key_name):
			for key,value in list(init_config.items(key_name)):
				parts = key.split("-")
				current = self.root[key_name]

				for i, part in enumerate(parts):
					is_last = i == len(parts) - 1
					if is_last:
						
						value,value_type,http_type,http_extra = set_type(value)
						current[part] = PersistentMapping()
						current[part]["value"] = value
						current[part]["type"] = value_type
						current[part]["http_type"] = http_type
						current[part]["http_extra"] = http_extra
						current[part]._p_changed = True
						transaction.commit()

					else:
						if part not in current:
							current[part] = PersistentMapping()

						current = current[part]
						

		config_dir = os.path.abspath(os.path.join(self.script_dir, '..', 'etc'))
		
		init_file = os.path.join(config_dir,"jdb_init.conf")
		
		init_config = configparser.ConfigParser()
		init_config.read(init_file)
		
		keys = list(init_config.items("main"))
		for key in keys:
			key_name = key[0]
		
			if key_name not in self.root:
				self.root[key_name] = PersistentMapping()
			if overwrite:
				self.root[key_name] = PersistentMapping()

			if key_name in init_config.sections():
				create_nested_key(key_name)
		transaction.commit()	

	def __init__(self,**kwargs):

		self.script_dir = os.path.dirname(os.path.abspath(__file__))
		run_dir = os.path.abspath(os.path.join(self.script_dir, '..', 'run'))
		#self.config_file = os.path.join(run_dir,"config.fs")
		#self.storage = ZODB.FileStorage.FileStorage(self.config_file)
		storage = ClientStorage.ClientStorage(('127.0.0.1', 8090))
		#self.db = ZODB.DB(self.storage)
		self.db = DB(storage)

		self.connection = self.db.open()
		self.root = self.connection.root()
		if "initialize" in kwargs:
			if kwargs["initialize"]:
				self.__populate__()
	
	def write(self,key,value):
		
		self.root[key] = value
		transaction.commit()

	def read(self,*keys):

		current = self.root
		for key in keys:
			if isinstance(current,Mapping) and key in current:
				current = current[key]
			else:
				if key in current:
					current = current[key]
					return True,current
				else:	
					return False, 0
		return True, current

	def get(self,*keys):
		return self.read(*keys)	

	def get_value(self,*keys):
		success, value = self.read(*keys)
		if success:
			return value
		else:
			logger.error("tried fetching key that doesn't exist (" + str(keys) + ")" )

	def __zodb_to_dict__(self,obj):
    		if isinstance(obj, Mapping):
        		return {k: self.__zodb_to_dict__(v) for k, v in obj.items()}
    		elif isinstance(obj, list):
        		return [self.__zodb_to_dict__(i) for i in obj]
    		else:
        		return obj
	def update(self,new_value,*keys):
		success, value = self.read(*keys)
		if not success:
			return False, "key doesn't exist"
		if "value" not in value:
			return False, "not a key with a value"

		try:
			value["value"] = new_value
			transaction.commit()
			return True, "sucess"
		except Exception as e:
			return False, "Error: " + str(e)

	def list(self):
		return list(self.root.keys())

	def get_all(self):
		
		return self.__zodb_to_dict__(self.root)
