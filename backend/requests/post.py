from config.config import db, app
from flask import request, jsonify
from models.post import Post, MediaType
from models.episode import Episode
from models.season import Season
from requests.image_service import save_image, delete_image
from config.constants import image_uploads, allowed_extensions

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
    ), 200

@app.route("/posts/create", methods=["POST"])
def create_post():
    description = request.form.get("description")
    media_type = request.form.get("media_type")
    episode_id = request.form.get("episode")
    season_id = request.form.get("season")

    media_type_enum = MediaType[media_type]
    file = request.files.get("media")

    filename, error = save_image(
        file,
        image_uploads,
        allowed_extensions
    )

    if error:
        return jsonify({"error": error}), 400

    episode = (
        Episode.query
        .join(Season)
        .filter(
            Season.id == season_id,
            Episode.id == episode_id
        )
        .first_or_404()  # raises 404 if not found
    )
    
    new_post = Post(media_url = filename,
                    description = description,
                    media_type = media_type_enum,
                    episode_id = episode.id,
                    episode = episode)
 
    try:
        db.session.add(new_post)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    new_post_id = new_post.id

    return jsonify({"id": new_post_id}), 201

