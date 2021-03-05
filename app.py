from flask import Flask, render_template, request, redirect

# connecting to databases (import)
from flask_sqlalchemy import SQLAlchemy

# import date time
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# connecting flask app to database
db = SQLAlchemy(app)


# defining model for db
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_stamp = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __ref__(self):
        return 'BlogPost: ' + str(self.id)


# basic routing in flask
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_stamp).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('update.html', post = post)

if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/home/<string:name>/posts/<int:id>')
# def hello(name, id):
#     return "<h1> Hello " + name + ", your id is: " + str(id) + "</h1>"


# # defining methods for routes
# @app.route('/onlyget', methods=['GET'])
# def only_get():
#     return "<h1> You can only get this page. </h1>"
