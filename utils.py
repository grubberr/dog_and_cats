
import sys
import datetime
from models import date_format

def get_birthday_or_exit(birthday):

    try:
        return datetime.datetime.strptime(birthday, date_format)
    except ValueError:
        print("incorrect birthday: %s" % birthday)
        sys.exit(1)
