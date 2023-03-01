from flask import Flask

def create():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')
    return app