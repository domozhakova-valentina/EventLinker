from flask import Flask
from flask_restful import Api
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


main_app = MyApp(__name__, static_folder="./../static")
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
