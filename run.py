import os

from Life import create_app, templates, db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager
app = create_app(os.getenv('FLASK_CONFIG','development'))

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# app.run(debug=True,template_folder=templates)
if __name__ == '__main__':
    manager.run()