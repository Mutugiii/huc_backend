from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import *

# Initializing the application with intended configurations
app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server)
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Profile=Profile, Post=Post, Comment=Comment, Like=Like, Follow=Follow)

if __name__ == '__main__':
    manager.run()