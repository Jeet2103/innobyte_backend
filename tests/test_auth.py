import logging
from app.logger import setup_logger

# Initialize logger for this test module
logger = setup_logger(__name__)

def test_register_and_login(test_client):
    """
    Test user registration and login functionality using Flask test client.
    Ensures:
    - User can register successfully.
    - User can log in and receive a valid access token.
    """
    logger.info("Starting test: test_register_and_login")

    # Attempt to register a new user
    try:
        res = test_client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123'
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data['user']['username'] == 'testuser'
        logger.info("User registration test passed.")
    except AssertionError as e:
        logger.error(f"User registration test failed. Response: {res.get_data(as_text=True)}")
        raise

    # Attempt to log in with the newly registered user
    try:
        res = test_client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'Testpass123'
        })
        assert res.status_code == 200
        assert 'access_token' in res.get_json()
        logger.info("User login test passed.")
    except AssertionError as e:
        logger.error(f"User login test failed. Response: {res.get_data(as_text=True)}")
        raise
