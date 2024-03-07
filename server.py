from app.app import main_app
from flask import render_template


@main_app.route('/', defaults={'path': ''})
@main_app.route('/a/<path:path>')
@main_app.route('/u/<path:path>')
def root(path):
    return render_template('base.html', title='EventLinker')


if __name__ == '__main__':
    main_app.run(port=5100, host='127.0.0.1', debug=True)
