from flask import Blueprint, render_template
from ..models import BlogPost
from ..extensions import db
from flask_login import current_user

static_views = Blueprint('static_views_bp', __name__, template_folder='templates')


@static_views.route('/')
def home():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    top_posts = posts[::-1][:5]
    return render_template(
        'index.html',
        all_posts=posts,
        rank=len(top_posts),
        top_posts=top_posts,
        current_user=current_user)


@static_views.route('/about')
def about():
    return render_template('about.html', current_user=current_user)


@static_views.route('/contact')
def contact():
    return render_template('contact.html', current_user=current_user)
