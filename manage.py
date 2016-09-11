import os 

from app import app,db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand 

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=8500))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()