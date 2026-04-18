from config.config import db, app
from flask import request, jsonify
from models.post import Post
from models.episode import Episode
from models.season import Season

@app.route("/posts", methods = ["GET"])
def get_posts():
    page_number = request.args.get("page", default=1, type=int)
    post_query = Post.query.join(Episode).join(Season)

    if "season_id" in request.args:
        season_id = request.args.get("season_id", type=int)
        post_query = post_query.filter(Season.id == season_id)
    
    if "episode_id" in request.args:
        episode_id = request.args.get("episode_id", type=int)
        post_query = post_query.filter(Episode.id == episode_id)

    posts = post_query.paginate(per_page=4, page=page_number)

    posts_to_json = list(map(lambda post: post.to_json(), posts.items))
    
    return jsonify(
        {
            "total": posts.total,
            "items": posts_to_json
        }
    )

@app.route("/movies/create", methods = ["POST"])
def movies_create():
    data = request.get_json()

    new_title = data.get("title")
    new_review = data.get("my_review")
    new_movie_category = data.get("category")
    new_rating = data.get("rating")
    new_imdb_link = data.get("imdb_link")
    new_release_year = data.get("release_year")

    new_movie_category_name = new_movie_category["name"]
    movie_category = MovieCategory.query.filter_by(name = new_movie_category_name).first()


    if not new_title:
        return jsonify(
            {
                "error": "a valid title is required"
            }
        ), 400
    if not movie_category:
        return jsonify(
            {
                "error": "a valid category is required"
            }
        ), 400
    new_movie = Movie(title = new_title,
                      my_review = new_review,
                      category = movie_category,
                      rating = new_rating,
                      imdb_link = new_imdb_link,
                      release_year = new_release_year)
    
    try:
        db.session.add(new_movie)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "error": str(e)
            }
        ), 400
    
    new_movie_id = new_movie.id
    return jsonify({"id": new_movie_id}), 200

@app.route("/movies", methods = ["DELETE"])
def delete_movie():
    data = request.get_json()
    ids = data.get("ids", [])

    if not ids:
        return jsonify({"error": "No IDs provided"}), 400

    movies = Movie.query.filter(Movie.id.in_(ids)).all()

    if not movies:
        return jsonify({"error": "No movie found"}), 404
    
    for movie in movies:
        db.session.delete(movie)

    db.session.commit()

    return jsonify({
        "deleted_ids": [t.id for t in movies]
    }), 200


@app.route("/movies/categories", methods = ["GET"])
def movies_categories():
    movies_cats = MovieCategory.query.all()
    movies_cats_to_json = list(map(lambda movie: movie.to_json(), movies_cats))

    return jsonify(
        movies_cats_to_json
    )


@app.route("/movies/category/create", methods = ["POST"])
def movie_category_create():
    new_name = request.json.get("name")

    same_category = MovieCategory.query.filter_by(name = new_name).first()
    if same_category:
        return jsonify(
            {
                "error": "a  movie category with same name already exists"
            }
        ), 400
    
    if not new_name:
        return jsonify(
            {
                "error": "A valid name is required"
            }
        ), 400
    
    new_movie_category = MovieCategory(name = new_name)
    
    try:
        db.session.add(new_movie_category)
        db.session.commit()
    
    except Exception as e:
        return jsonify(
            {
                "error": str(e) 
            }
        ), 400
    
    new_movie_category_id = new_movie_category.id
    return jsonify({"id": new_movie_category_id}), 201


@app.route("/movies/categories", methods = ["DELETE"])
def delete_movies_category():
    data = request.get_json()
    ids = data.get("ids", [])

    if not ids:
        return jsonify({"error": "No IDs provided"}), 400

    movies_cats = MovieCategory.query.filter(MovieCategory.id.in_(ids)).all()

    if not movies_cats:
        return jsonify({"error": "No categories found"}), 400
    
    for cat in movies_cats:
        db.session.delete(cat)

    db.session.commit()

    return jsonify({
        "deleted_ids": [t.id for t in movies_cats]
    }), 200