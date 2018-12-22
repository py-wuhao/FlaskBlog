import os
from flask_migrate import Migrate
from flask_script import Manager

from app import create_app, db

from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    manager.run()
