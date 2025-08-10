from common import *

#jdb = json_db()
jdb = json_db(initialize=True)


x = jdb.get_all()
pprint(x)
