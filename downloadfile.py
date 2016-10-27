import urllib
import os
import zipfile 
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler



def download():
    sports = urllib.URLopener()
    sports.retrieve("https://fantasydata.com/members/download-file.aspx?product=4885cd1b-6fd1-4db8-8c0a-47160973ca68", "file.zip")
    root = "/vagrant"
    zipfile.ZipFile("file.zip").extractall("sports")
    os.remove("file.zip")

if __name__ == "__main__":
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(download, "interval", hours=2)
    # scheduler.start()
    # try:
    #     pass
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown() 
    download()