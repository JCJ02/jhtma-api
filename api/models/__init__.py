from sqlalchemy.ext.declarative import declarative_base

# Shared Base for all models
Base = declarative_base()

# Import all models to include them in Base.metadata
# This ensures Alembic autogenerate works across all models

from api.models.users_model import Users, Accounts
from api.models.roles_model import Roles