from flask import Blueprint, request, jsonify
from app.models.comment import Comment
from app.extensions import db
from app.schemas.comment_schema import comment_schema, comments_schema
from app.utils.decorators import jwt_required_with_user
from app.logger import setup_logger
from flasgger import swag_from

# Initialize logger
logger = setup_logger(__name__)

# Define blueprint for comment-related routes
comment_bp = Blueprint('comments', __name__)


@comment_bp.route('/comments', methods=['POST'])
@jwt_required_with_user
@swag_from({
    'tags': ['Comments'],
    'summary': 'Create a comment',
    'description': 'Authenticated users can create a comment on a post.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'content': {'type': 'string'},
                'post_id': {'type': 'integer'}
            },
            'required': ['content', 'post_id']
        }
    }],
    'responses': {
        201: {'description': 'Comment created successfully'},
        400: {'description': 'Invalid input'},
        500: {'description': 'Internal server error'}
    }
})
def create_comment(current_user):
    if not request.is_json:
        logger.warning("Create comment failed: Invalid JSON")
        return jsonify({"error": "Missing or invalid JSON"}), 400

    try:
        data = request.get_json()
        content = data.get('content')
        post_id = data.get('post_id')

        if not content or not post_id:
            logger.warning("Create comment failed: Missing fields.")
            return jsonify({"error": "Content and post_id are required."}), 400

        comment = Comment(content=content, post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()

        logger.info(f"Comment created by user {current_user.id} on post {post_id}")
        return jsonify(comment_schema.dump(comment)), 201

    except Exception as e:
        logger.error(f"Error while creating comment: {e}")
        return jsonify({"error": "Failed to create comment"}), 500


@comment_bp.route('/comments', methods=['GET'])
@swag_from({
    'tags': ['Comments'],
    'summary': 'Get all comments (optionally by post)',
    'parameters': [{
        'name': 'post_id',
        'in': 'query',
        'type': 'integer',
        'required': False,
        'description': 'Filter comments by post ID'
    }],
    'responses': {
        200: {'description': 'Comments retrieved successfully'},
        500: {'description': 'Internal server error'}
    }
})
def get_comments():
    try:
        post_id = request.args.get('post_id')
        query = Comment.query

        if post_id:
            query = query.filter_by(post_id=post_id)
            logger.info(f"Fetching comments for post_id={post_id}")
        else:
            logger.info("Fetching all comments")

        comments = query.all()
        return jsonify(comments_schema.dump(comments)), 200

    except Exception as e:
        logger.error(f"Error retrieving comments: {e}")
        return jsonify({"error": "Failed to retrieve comments"}), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['GET'])
@swag_from({
    'tags': ['Comments'],
    'summary': 'Get a specific comment',
    'parameters': [{
        'name': 'comment_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the comment to fetch'
    }],
    'responses': {
        200: {'description': 'Comment retrieved successfully'},
        404: {'description': 'Comment not found'},
        500: {'description': 'Internal server error'}
    }
})
def get_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        logger.info(f"Fetched comment ID: {comment_id}")
        return jsonify(comment_schema.dump(comment)), 200

    except Exception as e:
        logger.error(f"Error fetching comment ID {comment_id}: {e}")
        return jsonify({"error": "Failed to retrieve comment"}), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required_with_user
@swag_from({
    'tags': ['Comments'],
    'summary': 'Update a comment',
    'parameters': [
        {
            'name': 'comment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the comment to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'content': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Comment updated successfully'},
        403: {'description': 'Unauthorized'},
        404: {'description': 'Comment not found'},
        500: {'description': 'Internal server error'}
    }
})
def update_comment(current_user, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author_id != current_user.id:
        logger.warning(f"User {current_user.id} unauthorized to update comment {comment_id}")
        return jsonify({"error": "Unauthorized."}), 403

    if not request.is_json:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    try:
        data = request.get_json()
        comment.content = data.get('content', comment.content)
        db.session.commit()

        logger.info(f"Comment {comment_id} updated by user {current_user.id}")
        return jsonify(comment_schema.dump(comment)), 200

    except Exception as e:
        logger.error(f"Error updating comment {comment_id}: {e}")
        return jsonify({"error": "Failed to update comment"}), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required_with_user
@swag_from({
    'tags': ['Comments'],
    'summary': 'Delete a comment',
    'parameters': [{
        'name': 'comment_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the comment to delete'
    }],
    'responses': {
        200: {'description': 'Comment deleted successfully'},
        403: {'description': 'Unauthorized'},
        404: {'description': 'Comment not found'},
        500: {'description': 'Internal server error'}
    }
})
def delete_comment(current_user, comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.author_id != current_user.id:
        logger.warning(f"User {current_user.id} unauthorized to delete comment {comment_id}")
        return jsonify({"error": "Unauthorized."}), 403

    try:
        db.session.delete(comment)
        db.session.commit()

        logger.info(f"Comment {comment_id} deleted by user {current_user.id}")
        return jsonify({"message": "Comment deleted."}), 200

    except Exception as e:
        logger.error(f"Error deleting comment {comment_id}: {e}")
        return jsonify({"error": "Failed to delete comment"}), 500
