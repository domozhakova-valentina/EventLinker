from flask import Flask
from flask_restful import Api
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from errors.handlers import errors
from api.users import UserResource, UsersListResource
from api.comments import CommentResource, CommentsListResource
from api.events import EventResource, EventsListResource
from api.likes import LikeResource


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = '23vghtklbn4hj8900'
        self.register_blueprint(errors)  # добавление своих ошибок 404, 403, 500
        # self.json_encoder = MyJSONEncoder
        # self.user_repo = SqliteUsersRepo("./db/redditclone.db")
        # # app.user_repo = InMemoryUsersRepo()
        # # self.post_repo = InMemoryPostsRepo()
        # self.post_repo = SqlitePostsRepo("./db/redditclone.db")
        # self.config['JWT_SECRET_KEY'] = 'super-secret'
        # self.config['JWT_EXPIRES'] = timedelta(hours=24)
        # self.config['JWT_HEADER_NAME'] = 'authorization'
        # self.config['JWT_IDENTITY_CLAIM'] = 'user'
        # self.api = Api(self)
        # self.jwt = JWTManager(self)


main_app = MyApp(__name__, static_folder="./../static")
fs_store = HttpExposedFileSystemStore('userimages', 'images/')
main_app.wsgi_app = fs_store.wsgi_middleware(main_app.wsgi_app)
# последние две строчки нужны для возможности сохранять изображения
api = Api(main_app)
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
