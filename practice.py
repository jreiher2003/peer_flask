import os
import requests
import time
from app import app, db, uploaded_photos
from app.nfl_stats.models import NFLTeam

# f = open('bills.jpg','wb')
# f.write(requests.get('https://upload.wikimedia.org/wikipedia/commons/c/ce/Buffalo_Bills_blue.png').content)
# f.close()
# download_photo("https://upload.wikimedia.org/wikipedia/commons/c/ce/Buffalo_Bills_blue.png", 'bills.png')

def save_all_team_pics():
    t = NFLTeam.query.all()
    for i in t:
        if i.WikipediaWordMarkUrl[-3:] == 'png':
            f = open("app/static/img/team_img/" + i.Name + ".png",'wb')
            f.write(requests.get(i.WikipediaWordMarkUrl).content)
            f.close()
            i.TeamImg = "team_img/"+i.Name+".png"
            db.session.add(i)
            db.session.commit()
           
        elif i.WikipediaWordMarkUrl[-3:] == 'svg':
            f = open("app/static/img/team_img/" + i.Name + '.svg', 'wb')
            f.write(requests.get(i.WikipediaWordMarkUrl).content)
            f.close
            i.TeamImg = "team_img/"+i.Name+".svg"
            db.session.add(i)
            db.session.commit()
            
        elif i.WikipediaWordMarkUrl[-3:] == 'jpg':
            f = open("app/static/img/team_img/" + i.Name + '.jpg', 'wb')
            f.write(requests.get(i.WikipediaWordMarkUrl).content)
            f.close 
            i.TeamImg = "team_img/"+i.Name+".jpg"
            db.session.add(i)
            db.session.commit()
           
        elif i.WikipediaWordMarkUrl[-3:] == 'gif':
            f = open("app/static/img/team_img/" + i.Name + '.gif', 'wb')
            f.write(requests.get(i.WikipediaWordMarkUrl).content)
            f.close
            i.TeamImg = "team_img/"+i.Name+".gif"
            db.session.add(i)
            db.session.commit()
            

        # print i.WikipediaWordMarkUrl, i.Name, i.TeamID
save_all_team_pics()


# avatar = uploaded_photos.save(i.Name+'.jpg', folder="team_img/")
# i.TeamImg = avatar
# db.add(i)
# db.commit()