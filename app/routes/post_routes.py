from flask import Blueprint, request, jsonify
from app.models.post import Post
from app.extensions import db
from app.schemas.post_schema import post_schema, posts_schema
from app.utils.decorators import jwt_required_with_user
from app.logger import setup_logger
from flasgger import swag_from

# Initialize logger for post routes
logger = setup_logger(__name__)

# Define blueprint for post-related routes
post_bp = Blueprint('posts', __name__)


@post_bp.route('/posts', methods=['POST'])
@jwt_required_with_user
@swag_from({
    'tags': ['Posts'],
    'summary': 'Create a new blog post',
    'description': 'Allows an authenticated user to create a blog post.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'content': {'type': 'string'}
            },
            'required': ['title', 'content']
        }
    }],
    'responses': {
        201: {'description': 'Post created successfully'},
        400: {'description': 'Missing required fields or invalid input'},
        500: {'description': 'Internal server error'}
    }
})
def create_post(current_user):
    if not request.is_json:
        logger.warning("Create post failed: Missing or invalid JSON.")
        return jsonify({"error": "Missing or invalid JSON"}), 400

    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            logger.warning("Create post failed: Title or content missing.")
            return jsonify({"error": "Title and content are required."}), 400

        new_post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        logger.info(f"Post created by user {current_user.id}: Post ID {new_post.id}")
        return jsonify(post_schema.dump(new_post)), 201

    except Exception as e:
        logger.error(f"Error creating post: {e}")
        return jsonify({"error": "Failed to create post"}), 500


@post_bp.route('/posts', methods=['GET'])
@swag_from({
    'tags': ['Posts'],
    'summary': 'Get all blog posts',
    'responses': {
        200: {'description': 'List of posts retrieved successfully'},
        500: {'description': 'Internal server error'}
    }
})
def get_posts():
    try:
        posts = Post.query.all()
        logger.info("Fetched all posts.")
        return jsonify(posts_schema.dump(posts)), 200
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return jsonify({"error": "Failed to retrieve posts"}), 500


@post_bp.route('/posts/<int:post_id>', methods=['GET'])
@swag_from({
    'tags': ['Posts'],
    'summary': 'Get a specific post by ID',
    'parameters': [{
        'name': 'post_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the post'
    }],
    'responses': {
        200: {'description': 'Post retrieved successfully'},
        404: {'description': 'Post not found'},
        500: {'description': 'Internal server error'}
    }
})
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        logger.info(f"Fetched post ID: {post_id}")
        return jsonify(post_schema.dump(post)), 200
    except Exception as e:
        logger.error(f"Error fetching post {post_id}: {e}")
        return jsonify({"error": "Failed to retrieve post"}), 500


@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required_with_user
@swag_from({
    'tags': ['Posts'],
    'summary': 'Update a blog post',
    'description': 'Only the author can update their post.',
    'parameters': [
        {
            'name': 'post_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the post to update'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'content': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Post updated successfully'},
        403: {'description': 'Unauthorized access'},
        404: {'description': 'Post not found'},
        500: {'description': 'Internal server error'}
    }
})
def update_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id:
        logger.warning(f"Unauthorized update attempt by user {current_user.id} on post {post_id}")
        return jsonify({"error": "Unauthorized."}), 403

    if not request.is_json:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    try:
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)

        db.session.commit()
        logger.info(f"Post {post_id} updated by user {current_user.id}")
        return jsonify(post_schema.dump(post)), 200

    except Exception as e:
        logger.error(f"Error updating post {post_id}: {e}")
        return jsonify({"error": "Failed to update post"}), 500


@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required_with_user
@swag_from({
    'tags': ['Posts'],
    'summary': 'Delete a blog post',
    'description': 'Only the author can delete their post.',
    'parameters': [{
        'name': 'post_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the post to delete'
    }],
    'responses': {
        200: {'description': 'Post deleted successfully'},
        403: {'description': 'Unauthorized access'},
        404: {'description': 'Post not found'},
        500: {'description': 'Internal server error'}
    }
})
def delete_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id:
        logger.warning(f"Unauthorized delete attempt by user {current_user.id} on post {post_id}")
        return jsonify({"error": "Unauthorized."}), 403

    try:
        db.session.delete(post)
        db.session.commit()
        logger.info(f"Post {post_id} deleted by user {current_user.id}")
        return jsonify({"message": "Post deleted."}), 200

    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {e}")
        return jsonify({"error": "Failed to delete post"}), 500
