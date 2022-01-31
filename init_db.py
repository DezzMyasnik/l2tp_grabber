from datetime import datetime

from pony.orm import *

DB_CONFIG = {'provider': 'sqlite', 'filename': r'database.sqlite', 'create_db': 'True'}
db = Database()
db.bind(DB_CONFIG)


class SMS_text(db.Entity):
    time_of_sms = Optional(datetime)
    From_phone_num = Optional(str)
    To_phone_num = Optional(str)
    sms_text = Optional(str)
    multipart = Optional(str)


db.generate_mapping(create_tables=True)
