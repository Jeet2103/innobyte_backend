import os
from pathlib import Path

def create_flask_blog_structure():
    """Create the Flask blog API directory structure in the current directory."""
    
    # Define the directory structure
    structure = {
        "app": {
            "__init__.py": "",
            "config.py": "",
            "extensions.py": "",
            "logger.py": "",
            "models": {
                "__init__.py": "",
                "user.py": "",
                "post.py": "",
                "comment.py": ""
            },
            "schemas": {
                "__init__.py": "",
                "user_schema.py": "",
                "post_schema.py": "",
                "comment_schema.py": ""
            },
            "routes": {
                "__init__.py": "",
                "auth_routes.py": "",
                "post_routes.py": "",
                "comment_routes.py": ""
            },
            "services": {
                "__init__.py": "",
                "auth_service.py": ""
            },
            "utils": {
                "__init__.py": "",
                "decorators.py": ""
            }
        },
        "migrations": {
            "env.py": "",
            "README": "",
            "script.py.mako": "",
            "versions": {
                "20250708_initial_migration.py": ""
            }
        },
        "tests": {
            "__init__.py": "",
            "conftest.py": "",
            "test_auth.py": "",
            "test_posts.py": "",
            "test_comments.py": ""
        },
        ".env": "",
        ".gitignore": "",
        "README.md": "",
        "requirements.txt": "",
        "run.py": "",
        "wsgi.py": ""
    }

    def create_structure(directory, structure):
        """Recursively create the directory structure."""
        for name, content in structure.items():
            path = Path(directory) / name
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, 'w') as f:
                    if content:
                        f.write(content)

    # Create the structure in current directory
    create_structure(".", structure)

    print("Flask blog API structure created in current directory")

if __name__ == "__main__":
    create_flask_blog_structure()