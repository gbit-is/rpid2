import os
import logging
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

class foojson_db():

        def __init__(self):

                dir_map = get_dir_map()
                config_dir = dir_map["run"]
                self.config_file = os.path.join(config_dir,"config.fs")

                self.storage = ZODB.FileStorage.FileStorage(self.config_file)
                self.db = ZODB.DB(self.storage)
                self.connection = self.db.open()
                self.root = self.connection.root()

        def write(self,key,value):

                self.root[key] = value

        def read(self,key):

                value = self.root[key]

jdb = foojson_db()
