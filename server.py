from waitress import serve
from app.app import main_app

from flask_login import LoginManager
from data.users import User
import logging
from data import db_session

from routes.form_r import form
from routes.user_r import rusers
from routes.event_r import revent

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(main_app)

# регистрируем все пути
main_app.register_blueprint(form)
main_app.register_blueprint(rusers)
main_app.register_blueprint(revent)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    serve(main_app, host="127.0.0.1", port=8000)
