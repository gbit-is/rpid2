from common import *
from json_db import *

logger = get_logger("bootstrap")


jdb = json_db(initialize=True)
pprint (jdb.get_all())


