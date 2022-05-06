import logging
from logging.handlers import RotatingFileHandler
import os

from app.myglobals import logfolder

####
import datetime
import tzlocal
from dateutil import tz

class MyFormatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    localzone_name = tzlocal.get_localzone_name()
    # print('==localzone_name==', localzone_name)
    def converter(self, timestamp):
        print('==timestamp==', timestamp)
        # dt = datetime.datetime.fromtimestamp(timestamp)
        # 1.aws gecloud1 timezone is "Etc/UTC"
        # 2.china timezone is "Asia/Shanghai"
        # return dt.replace(tzinfo=tz.gettz(MyFormatter.localzone_name)).astimezone(tz=tz.gettz('Asia/Shagnhai'))
        return dt

    def formatTime(self, record, datefmt="%Y-%m-%d %H:%M:%S.%f"):
        dt = self.converter(record.created)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")
####

logfile = os.path.abspath(os.path.join(logfolder, "log.txt"))

# logger init
logger = logging.getLogger(__name__)


# logger config
logger.setLevel(level = logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# todo
# formatter = MyFormatter('%(asctime)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler(logfile, maxBytes = 1*1024*100, backupCount=3)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)

