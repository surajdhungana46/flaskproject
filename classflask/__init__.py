from flask import Flask
# from flask_script import Command
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
app = Flask(__name__)
app.config['SECRET_KEY'] = 'surajdhungana9823040065'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt=Bcrypt(app)

# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view = "login"



from classflask import routes

