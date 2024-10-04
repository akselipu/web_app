from flask import render_template, url_for, flash, redirect, request
from app import app
from datisbase import db

from sqlalchemy.sql import text
import users
from users import login_required  

from flask import render_template, request, redirect, session, url_for


@app.route("/")

def index():
    # Fetch posts along with their comments
    comments_sql = text("""
        SELECT c.content, c.post_id, u.name 
        FROM comments c
        JOIN users u ON c.author_id = u.id
        ORDER BY c.created_at ASC
    """)
    comments = db.session.execute(comments_sql).fetchall()

    posts_sql = text("""
        SELECT p.id, p.title, p.content, p.author_id, p.category_id, p.created_at, u.name AS author_name, c.name AS category_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
    """)
    posts = db.session.execute(posts_sql).fetchall()

    # Prepare a list to hold posts with their corresponding tags
    posts_with_tags = []
    # Iterate over each post and fetch its associated tags
    for post in posts:
        # Fetch the tags for the current post
        tags_sql = text("""
            SELECT t.name
            FROM tags t
            JOIN post_tags pt ON t.id = pt.tag_id
            WHERE pt.post_id = :post_id
        """)
        tags = db.session.execute(tags_sql, {"post_id": post.id}).fetchall()

        # Create a dictionary to hold post information along with its tags
        post_with_tags = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_name": post.author_name,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "category_id": post.category_id,
            "category_name": post.category_name,
            "tags": [tag[0] for tag in tags]  # Extract the tag names from the result
        }

        # Append the post with tags to the list
        posts_with_tags.append(post_with_tags)


    # Fetch categories from the database
    categories_sql = text("SELECT * FROM categories")
    categories = db.session.execute(categories_sql).fetchall()
  

    # Pass posts and comments to the template
    return render_template("index.html", posts=posts_with_tags, comments=comments, categories=categories)

# Register new user
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
            return render_template("error.html", message="Username already in use")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Password mismatch!")
        if password1 == "":
            return render_template("error.html", message="Password empty")

        """role = request.form["role"]
        
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")
        """
        if not users.register(username, password1):
           return render_template("error.html", message="Registering unsuccessful")
        
        return redirect("/")
    

# Login function
@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        
        if not users.login(username, password):
            return render_template("error.html", message="Wrong username or password")
        
        return redirect("/")
    
# Function to see posts in their respective categories
@app.route("/posts/category/<int:category_id>")
def posts_by_category(category_id):
    posts_sql = text("""
        SELECT p.id, p.title, p.content, p.author_id, created_at, p.category_id, u.name AS author_name, c.name AS category_name 
        FROM posts p 
        JOIN users u ON p.author_id = u.id 
        JOIN categories c ON p.category_id = c.id 
        WHERE p.category_id = :category_id 
        ORDER BY p.created_at DESC
    """)
    posts = db.session.execute(posts_sql, {"category_id": category_id}).fetchall()

    # Fetch comments for these posts
    comments_sql = text("""
        SELECT c.content, c.post_id, u.name 
        FROM comments c
        JOIN users u ON c.author_id = u.id
        WHERE c.post_id IN (SELECT id FROM posts WHERE category_id = :category_id)
        ORDER BY c.created_at ASC
    """)
    comments = db.session.execute(comments_sql, {"category_id": category_id}).fetchall()

        # Fetch tags for the posts in the selected category
    tags_sql = text("""
        SELECT pt.post_id, t.name AS tag_name
        FROM post_tags pt
        JOIN tags t ON pt.tag_id = t.id
        WHERE pt.post_id IN (SELECT id FROM posts WHERE category_id = :category_id)
    """)
    tags = db.session.execute(tags_sql, {"category_id": category_id}).fetchall()

    # Create a mapping of post IDs to their tags
    post_tags = {}
    for tag in tags:
        post_id = tag[0]  # Adjust to access the correct index
        tag_name = tag[1]  # Adjust to access the correct index
        if post_id not in post_tags:
            post_tags[post_id] = []
        post_tags[post_id].append(tag_name)


    # Fetch all categories for the category filter dropdown
    categories_sql = text("SELECT * FROM categories")
    categories = db.session.execute(categories_sql).fetchall()

    return render_template("index.html", posts=posts, comments=comments, post_tags=post_tags, categories=categories)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/delete_account", methods=["POST"])
def delete_account():
    
    if not session.get("user_id"):
        return redirect("/login")
    
    user_id = session.get("user_id")
    user_name = session.get("user_name") 
    
    
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

        # To drop user revoke all privileges
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
@login_required
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category_id = request.form["category_id"]
        author_id = session.get("user_id")
        tags_input = request.form.get("tags")

        try:
            # Insert the post into the posts table
            post_sql = text("""
                INSERT INTO posts (title, content, category_id, author_id)
                VALUES (:title, :content, :category_id, :author_id) RETURNING id
            """)
            result = db.session.execute(post_sql, {
                "title": title,
                "content": content,
                "category_id": category_id,
                "author_id": author_id
            })
            post_id = result.fetchone()[0]

            # Handle tags
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",")]
                
                for tag_name in tags:
                    # Insert the tag into the tags table if it doesn't exist
                    tag_sql = text("""
                        INSERT INTO tags (name)
                        VALUES (:tag_name)
                        RETURNING id
                    """)
                    tag_result = db.session.execute(tag_sql, {"tag_name": tag_name})
                    tag_id_row = tag_result.fetchone()


                    # If the tag already exists, fetch its ID
                    if tag_id_row:  
                        tag_id = tag_id_row[0]
                    else:
                        # If the tag doesn't exist, insert it and get the new tag ID
                        tag_id = db.session.execute(
                            text("INSERT INTO tags (name) VALUES (:tag_name) RETURNING id"),
                            {"tag_name": tag_name}
                        ).fetchone()[0]  

                   
                    post_tag_sql = text("""
                        INSERT INTO post_tags (post_id, tag_id)
                        VALUES (:post_id, :tag_id)
                    """)
                    db.session.execute(post_tag_sql, {"post_id": post_id, "tag_id": tag_id})

            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}") # Print error to help debug
            return render_template("error.html", message="An error occurred while trying to create the post.")

    return render_template("create_post.html")


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

    # Get the current category_id
    category_id = request.args.get('category_id')

    # If the page is filtered by category, redirect to the filtered category page
    if category_id:
        return redirect(url_for('posts_by_category', category_id=category_id, _anchor=f"post-{post_id}"))
    
    # Otherwise, redirect back to the homepage
    return redirect(url_for('index', _anchor=f"post-{post_id}"))


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    # Fetch the post from the database
    post = db.session.execute(text("SELECT * FROM posts WHERE id = :post_id"), {"post_id": post_id}).fetchone()

    if not post:
        return render_template("error.html", message="Post not found")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # Update the post in the database
        sql = text("UPDATE posts SET title = :title, content = :content WHERE id = :post_id")
        db.session.execute(sql, {"title": title, "content": content, "post_id": post_id})
        db.session.commit()

        return redirect("/")

    # Render the form with the existing post data
    return render_template("edit_post.html", post=post)
