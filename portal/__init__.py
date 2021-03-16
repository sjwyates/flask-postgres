from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sassutils.wsgi import SassMiddleware
from flask_login import LoginManager
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # @todo: disable in production
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'portal': ('static/scss', 'static/css', '/static/css')
    })

    with app.app_context():
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import PortalUser

    @login_manager.user_loader
    def load_user(user_id):
        return PortalUser.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command('db', MigrateCommand)

    return app
