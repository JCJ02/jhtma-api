from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from api.configurations.configuration import configuration

# SYNCHRONOUS POSTGRESQL CONNECTION (USING PSYCOPG2)
DATABASE_URL = configuration["database"].get("url")

# CREATE SYNCHRONOUS ENGINE
engine = create_async_engine(DATABASE_URL, echo = True)

# CREATE SESSION FACTORY
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# Singleton pattern for database session management
class DatabaseSessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSessionManager, cls).__new__(cls)
            cls._instance.session_factory = async_session_factory
        return cls._instance

    def session(self) -> AsyncSession:
        """Create a new database session."""
        return self.session_factory()

# Export the singleton instance of the session manager
db_session_manager = DatabaseSessionManager()

# Dependency for FastAPI Routes
async def get_database():
    async with db_session_manager.session() as session:
        yield session