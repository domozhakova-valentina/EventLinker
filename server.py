from app.app import MyApp

from flask_login import LoginManager
from data.users import User
import logging

from flask_restful import Api

from api.users import UserResource, UsersListResource
from api.comments import CommentResource, CommentsListResource
from api.events import EventResource, EventsListResource
from api.likes import LikeResource
from data import db_session

from routes.form_r import form
from routes.user_r import rusers
from routes.event_r import revent

app = MyApp(__name__, static_folder="static", template_folder="app/templates")
# регистрируем все пути
app.register_blueprint(form)
app.register_blueprint(rusers)
app.register_blueprint(revent)

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


api = Api(app)
db_session.global_init("db/event_linker.db")
# для пользователей
api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')
# для событий
api.add_resource(EventsListResource, '/api/v2/events')
api.add_resource(EventResource, '/api/v2/events/<int:event_id>')
# для комментариев
api.add_resource(CommentsListResource, '/api/v2/comments')
api.add_resource(CommentResource, '/api/v2/comments/<int:comment_id>')
# для лайков
api.add_resource(LikeResource, '/api/v2/like/<int:event_id>')


if __name__ == '__main__':
    app.run()
