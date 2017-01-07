"""
A script that pops db with imgs strings
"""
import os
import requests
import time
from app import app, db, uploaded_photos
from app.nfl_stats.models import NFLTeam

def save_all_team_pics():
    t = NFLTeam.query.all()
    for i in t:
        if i.WikipediaWordMarkUrl[-3:] == 'png':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/team_img/" + i.Name + ".png",'wb')
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close()
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/team_img/" + i.Name + ".png", "wb")
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close()
        elif i.WikipediaWordMarkUrl[-3:] == 'svg':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/team_img/" + i.Name + '.svg', 'wb')
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/team_img/" + i.Name + ".svg", "wb")
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close()
            
        elif i.WikipediaWordMarkUrl[-3:] == 'jpg':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/team_img/" + i.Name + '.jpg', 'wb')
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close 
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/team_img/" + i.Name + ".jpg", "wb")
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close()
           
        elif i.WikipediaWordMarkUrl[-3:] == 'gif':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/team_img/" + i.Name + '.gif', 'wb')
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/team_img/" + i.Name + ".gif", "wb")
                f.write(requests.get(i.WikipediaWordMarkUrl).content)
                f.close()
                 
def save_all_nfl_logos():
    t = NFLTeam.query.all()
    for i in t:
        if i.WikipediaLogoUrl[-3:] == 'png':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/nfl_logo/" + i.Name + ".png",'wb')
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close()
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/nfl_logo/" + i.Name + ".png", "wb")
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close()
        elif i.WikipediaLogoUrl[-3:] == 'svg':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/nfl_logo/" + i.Name + '.svg', 'wb')
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/nfl_logo/" + i.Name + ".svg", "wb")
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close()
            
        elif i.WikipediaLogoUrl[-3:] == 'jpg':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/nfl_logo/" + i.Name + '.jpg', 'wb')
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close 
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/nfl_logo/" + i.Name + ".jpg", "wb")
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close()
           
        elif i.WikipediaLogoUrl[-3:] == 'gif':
            if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
                f = open("app/static/img/nfl_logo/" + i.Name + '.gif', 'wb')
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close
            elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
                f = open("/var/www/peer_flask/img/nfl_logo/" + i.Name + ".gif", "wb")
                f.write(requests.get(i.WikipediaLogoUrl).content)
                f.close()


if __name__ == "__main__":
    save_all_team_pics()
    save_all_nfl_logos()


