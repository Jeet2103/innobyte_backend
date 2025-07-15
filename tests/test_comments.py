from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def test_create_and_delete_comment(test_client):
    """
    Test full comment lifecycle:
    - Register and authenticate a user.
    - Create a post.
    - Add a comment to that post.
    - Delete the comment.
    """
    logger.info("Starting test: test_create_and_delete_comment")

    try:
        # Register a user
        register_res = test_client.post('/api/auth/register', json={
            'username': 'commenter',
            'email': 'commenter@example.com',
            'password': 'Pass1234'
        })

        # Login the user and get JWT token
        login_res = test_client.post('/api/auth/login', json={
            'username': 'commenter',
            'password': 'Pass1234'
        })
        token = login_res.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        logger.info("User registered and authenticated successfully.")
    except Exception as e:
        logger.error(f"Auth setup failed: {e}")
        raise

    try:
        # Create a post
        post_res = test_client.post('/api/posts', json={
            'title': 'Post for comment',
            'content': 'Some content'
        }, headers=headers)
        post_id = post_res.get_json()['id']
        logger.info(f"Post created successfully with ID {post_id}.")
    except Exception as e:
        logger.error(f"Post creation failed: {e}")
        raise

    try:
        # Add a comment to the post
        comment_res = test_client.post('/api/comments', json={
            'post_id': post_id,
            'content': 'Nice post!'
        }, headers=headers)
        assert comment_res.status_code == 201
        comment_id = comment_res.get_json()['id']
        logger.info(f"Comment created successfully with ID {comment_id}.")
    except AssertionError as e:
        logger.error(f"Comment creation failed. Response: {comment_res.get_data(as_text=True)}")
        raise

    try:
        # Delete the comment
        delete_res = test_client.delete(f'/api/comments/{comment_id}', headers=headers)
        assert delete_res.status_code == 200
        logger.info(f"Comment with ID {comment_id} deleted successfully.")
    except AssertionError as e:
        logger.error(f"Comment deletion failed. Response: {delete_res.get_data(as_text=True)}")
        raise
