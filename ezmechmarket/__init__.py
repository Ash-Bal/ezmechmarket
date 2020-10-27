import os

from flask import Flask

def create_app(test_config=None):
    # create and cofigure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=b'i\x03\x8e\x0e)`8B\xc9s\xdb(\x1d\xb4\xd8y',
        DATABASE=os.path.join(app.instance_path, 'ezmechmarket.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    if __name__ == "__main__":
        app.run(ssl_context='adhoc')

    from . import db
    db.init_app(app)

    from . import market
    app.register_blueprint(market.bp)
    app.add_url_rule('/', endpoint='index')

    from . import imgurinit
    
    return app
