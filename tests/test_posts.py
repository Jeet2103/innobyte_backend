from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def test_create_read_update_delete_post(test_client):
    """
    Test the complete post lifecycle:
    - Register and authenticate a user
    - Create a post
    - Read the created post
    - Update the post
    - Delete the post
    """
    logger.info("Starting test: test_create_read_update_delete_post")

    try:
        # Register and login
        test_client.post('/api/auth/register', json={
            'username': 'author',
            'email': 'author@example.com',
            'password': 'Pass1234'
        })
        login_res = test_client.post('/api/auth/login', json={
            'username': 'author',
            'password': 'Pass1234'
        })
        token = login_res.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        logger.info("User registered and logged in successfully.")
    except Exception as e:
        logger.error(f"User authentication failed: {e}")
        raise

    try:
        # Create post
        create_res = test_client.post('/api/posts', json={
            'title': 'First Post',
            'content': 'Post content'
        }, headers=headers)
        assert create_res.status_code == 201
        post_id = create_res.get_json()['id']
        logger.info(f"Post created successfully with ID {post_id}.")
    except AssertionError as e:
        logger.error(f"Post creation failed. Response: {create_res.get_data(as_text=True)}")
        raise

    try:
        # Read post
        read_res = test_client.get(f'/api/posts/{post_id}')
        assert read_res.status_code == 200
        assert read_res.get_json()['title'] == 'First Post'
        logger.info(f"Post read successfully with title: {read_res.get_json()['title']}")
    except AssertionError as e:
        logger.error(f"Post read failed. Response: {read_res.get_data(as_text=True)}")
        raise

    try:
        # Update post
        update_res = test_client.put(f'/api/posts/{post_id}', json={
            'title': 'Updated Post'
        }, headers=headers)
        assert update_res.status_code == 200
        assert update_res.get_json()['title'] == 'Updated Post'
        logger.info(f"Post updated successfully to title: {update_res.get_json()['title']}")
    except AssertionError as e:
        logger.error(f"Post update failed. Response: {update_res.get_data(as_text=True)}")
        raise

    try:
        # Delete post
        delete_res = test_client.delete(f'/api/posts/{post_id}', headers=headers)
        assert delete_res.status_code == 200
        logger.info(f"Post with ID {post_id} deleted successfully.")
    except AssertionError as e:
        logger.error(f"Post deletion failed. Response: {delete_res.get_data(as_text=True)}")
        raise
