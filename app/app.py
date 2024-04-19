from flask import Flask
from errors.handlers import errors


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = '23vghtklbn4hj8900'
        self.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////db/event_linker.db"
        self.register_blueprint(errors)  # добавление своих ошибок 404, 403, 500
