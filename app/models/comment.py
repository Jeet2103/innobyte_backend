from app.extensions import db
from app.logger import setup_logger

# Initialize logger for the Comment model
logger = setup_logger(__name__)

class Comment(db.Model):
    """Model representing a comment made by a user on a post."""
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the comment
    content = db.Column(db.Text, nullable=False)  # Comment text content
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Associated post
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Commenting user
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp of creation

    def __repr__(self):
        return f"<Comment {self.id} on Post {self.post_id}>"

# Log that the Comment model was loaded
logger.info("Comment model loaded and mapped to table 'comments'")
