from app.init_app import app,init_app, manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from app.imagenet import init_net

if __name__ == "__main__":
    init_app(app)
    init_net(app)
    manager.run()