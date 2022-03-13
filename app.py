##### IMPORTS #####
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import PostForm, SearchForm
from datetime import datetime
from flask_ckeditor import CKEditor

import os

##### INITIALISATION #####
app = Flask(__name__)
ckeditor = CKEditor(app)

##### CONFIG ######
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"

##### CONNECT DB #####
db = SQLAlchemy(app)


##### DATABASE MODELS #####
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post, '{self.title}', On {self.date}"


##### Pass secretkey to extended files #####
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


##### ROUTES ######
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=posts)

@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash("Post Created Successfully", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", action="New Post", form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post Has Been Updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", action="Update Post", form=form)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted successfully", "success")
    return redirect(url_for("home"))

# Search
@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    posts = Post.query
    page = request.args.get("page", 1, type=int)

    if form.validate_on_submit:
        post.searched = form.searched.data

        posts = posts.filter(Post.content.like("%" + post.searched + "%"))
        posts = posts.order_by(Post.date.desc()).paginate(page=page, per_page=5)

        return render_template("search.html", form=form, searched=post.searched, posts=posts)


##### ERROR HANDLER ROUTE #####
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", title="Page not found"), 404


##### RUN APP #####
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
