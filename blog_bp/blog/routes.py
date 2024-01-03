from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from flask_gravatar import Gravatar
from datetime import date
from ..forms import CreatePostForm, CommentForm
from ..models import BlogPost, Comment
from ..extensions import db


blog = Blueprint(
    'blog_bp', __name__, template_folder='templates'
)

gravatar = Gravatar(blog,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# todo: display all blog post and involve pagination and current_user
@blog.route('/all')
@login_required
def get_all_posts():
    return


@blog.route('/<int:post_id>', methods=["GET", "POST"])
@login_required
def single_post(post_id):
    form = CommentForm()
    post = db.get_or_404(BlogPost, post_id)
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to register or login to comment')
            return redirect(url_for("user_bp.login"))
        comment = Comment(
            text=form.comment.data,
            post=post,
            user=current_user
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(request.url)

    return render_template(
        'post.html', post=post, length=len(post.post_comments), all_posts=posts[::-1][:5], form=form, current_user=current_user)


@blog.route('/new', methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('static_views_bp.home'))
    return render_template('make-post.html', form=form, current_user=current_user)


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        img_url=post.img_url,
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.title.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('single_post', post_id=post_id))
    return render_template('make-post.html', form=form, current_user=current_user, is_edit=True)


@blog.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
