from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


#
# all_posts = [
#     {'title': 'Post 1',
#      'content': 'This is the content',
#      'author': 'Emilio'},
#     {'title': 'Post 2',
#      'content': 'This is the content for post 2'}
# ]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/<string:name>/posts/<int:id_vip>')
def hello_world(name, id_vip):
    return "Hello World! My name is  " + name + " and my id is " + str(id_vip)


@app.route('/onlyget', methods=['GET'])
def onlyget():
    return " This is an only GET requests page "


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        post_new = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(post_new)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == '__main__':
    app.run()
