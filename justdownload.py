import os 
import urllib
import urllib2
from datetime import datetime 
import zipfile


print('The time is: %s\r\n' % datetime.now())
myip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
print "your IP Address is: ",  myip


sports = urllib.URLopener()
sports.retrieve(os.environ["FD_URL"], "file.zip")
if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
    print "Development download starting now..."
    root = os.getcwd()
    path = root + "/file.zip"
    print path
    zipfile.ZipFile("file.zip").extractall("sports")
    os.remove("file.zip")
elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
    print "Production Download starting now..."
    # root = os.getcwd()
    # uid = pwd.getpwnam("finn").pw_uid
    # gid = grp.getgrnam("finn").gr_gid
    # path = "/home/finn/www/peer_flask" + "/file.zip"
    # print path
    # os.chown(path, uid, gid)
    zipfile.ZipFile("file.zip").extractall("sports")
    os.remove("file.zip")