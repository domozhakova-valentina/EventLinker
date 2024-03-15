from flask import Flask
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = '23vghtklbn4hj8900'
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