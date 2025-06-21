import os
from dotenv import load_dotenv
from string import Template

# Load environment variables from .env file
load_dotenv()

def resolve_nested_env(value):
    return Template(value).substitute(os.environ) if value else value

configuration = {
    "app": {
        "port": int(os.getenv("PORT", 8080)),
        "env": os.getenv("PROJECT_ENV", "development"),
    },
    "database": {
        "url": os.getenv("DATABASE_URL")
    },
    "key": {
        "secretKey": os.getenv("JWT_SECRET_KEY", "default_jwt_secret"),
        "x_key": os.getenv("API_KEY", "default_api_key"),
        "refreshKey": os.getenv("JWT_REFRESH_SECRET_KEY", "default_refresh_secret"),
        "expiresIn": os.getenv("JWT_EXPIRES_IN", "3600"), # Default to 1 hour
        "refreshExpiresIn": os.getenv("JWT_REFRESH_EXPIRES_IN", "86400"), # Default to 24 hours
    },
    "url": {
        "local": f"http://localhost:{os.getenv('PORT', 8000)}/api/v1",
        "forward": f"{os.getenv('PORT_FORWARD_URL', '')}/api/v1",
    },
}