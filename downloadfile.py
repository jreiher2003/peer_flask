import urllib
import os
import zipfile 
from datetime import datetime
import time
from apscheduler.scheduler.background import BackgroundScheduler



def download():
    sports = urllib.URLopener()
    sports.retrieve("https://fantasydata.com/members/download-file.aspx?product=730dbec5-4ea1-4c56-888f-446f8f5560c6", "file.zip")
    root = "/vagrant"
    zipfile.ZipFile("file.zip").extractall("sports")
    os.remove("file.zip")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(download, "interval", hours=2)
    scheduler.start()
    try:
        pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() 