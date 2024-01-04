from flask import Flask
from flask_bootstrap import Bootstrap5
from blog_bp.extensions import db, login_manager
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
import os

# BLUEPRINTS
from blog_bp.static_views.routes import static_views
from blog_bp.blog.routes import blog
from blog_bp.users.routes import user_bp

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()


# Register blueprint template
app.register_blueprint(static_views)
app.register_blueprint(user_bp)
app.register_blueprint(blog, url_prefix='/post')

if __name__ == '__main__':
    app.run(debug=True)
