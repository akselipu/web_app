from flask import render_template, url_for, flash, redirect, request
from app import app
from datisbase import db
#from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql import text
import users
from users import login_required  # Assume you have a login_required decorator
from datisbase import BlogPost
from flask import render_template, request, redirect, session, url_for


@app.route("/")

def index():
    # Fetch posts along with their comments
    posts_sql = text("SELECT * FROM posts ORDER BY created_at DESC")
    posts = db.session.execute(posts_sql).fetchall()

    comments_sql = text("""
        SELECT c.content, c.post_id, u.name 
        FROM comments c
        JOIN users u ON c.author_id = u.id
        ORDER BY c.created_at ASC
    """)
    comments = db.session.execute(comments_sql).fetchall()

    # Pass posts and comments to the template
    return render_template("index.html", posts=posts, comments=comments)

@app.route("/register", methods=['get', 'post'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        # Check if username already exists
        existing_user = users.get_user_by_username(username)
        if existing_user:
            return render_template("error.html", message="Käyttäjänimi on jo käytössä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        role = request.form["role"]
        
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")
        
        if not users.register(username, password1, role):
           return render_template("error.html", message="Rekisteröinti ei onnistunut")
        
        return redirect("/")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        
        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/delete_account", methods=["POST"])
def delete_account():
    
    if not session.get("user_id"):
        return redirect("/login")
    
    user_id = session.get("user_id")
    user_name = session.get("user_name")  # Get the username to drop the role
    
    
    try:
        # Delete user's posts
        delete_posts = text("DELETE FROM posts WHERE author_id = :user_id")
        db.session.execute(delete_posts, {"user_id": user_id})
        
        # Delete user's comments
        delete_comments = text("DELETE FROM comments WHERE author_id = :user_id")
        db.session.execute(delete_comments, {"user_id": user_id})
        

        # Finally, delete the user
        delete_user = text("DELETE FROM users WHERE id = :user_id")
        db.session.execute(delete_user, {"user_id": user_id})


        try:
            revoke_user = text("REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "+user_name)
            db.session.execute(revoke_user, {"username": user_name})
        except Exception:
            pass

        
        drop_role_sql = text("DROP ROLE IF EXISTS "+user_name)
        print(drop_role_sql)
        db.session.execute(drop_role_sql, {"username": user_name})
        
    
        db.session.commit()
        
        # Clear the session and log the user out
        session.clear()
        
        return redirect("/")
    
    except Exception as e:
        return render_template("error.html", message="An error occurred while trying to delete the account.")


@app.route("/create_post", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in
def create_post():
    if request.method == "POST":
        # Get the post data
        title = request.form.get("title")
        content = request.form.get("content")
        
        # Check if the fields are filled
        if not title or not content:
            return render_template("error.html", message="Title and content are required")

        # Create a new blog post instance
        new_post = BlogPost(title=title, content=content, author_id=session["user_id"])

        # Add it to the database
        db.session.add(new_post)
        db.session.commit()

        # Redirect to home page or wherever you want
        return redirect("/")

    # Render the post creation form
    return render_template("create_post.html")

@app.route("/post/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    # Fetch the post (assuming you already have a 'posts' model)
    post = BlogPost.query.get_or_404(post_id)

    # Fetch the comments related to the post using raw SQL
    sql = text("SELECT c.content, u.name, c.created_at FROM comments c JOIN users u ON c.author_id = u.id WHERE c.post_id = :post_id ORDER BY c.created_at DESC")
    result = db.session.execute(sql, {"post_id": post_id})
    comments = result.fetchall()

    return render_template("post.html", post=post, comments=comments)

@app.route("/add_comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    if "user_id" not in session:
        return render_template("error.html", message="You need to log in to add a comment")

    content = request.form["content"]
    if len(content) < 1:
        return render_template("error.html", message="Comment cannot be empty")

    author_id = session["user_id"]
    sql = text("INSERT INTO comments (content, post_id, author_id) VALUES (:content, :post_id, :author_id)")
    db.session.execute(sql, {"content": content, "post_id": post_id, "author_id": author_id})
    db.session.commit()

    return redirect("/")