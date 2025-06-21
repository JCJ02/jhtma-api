from api.repositories.test_repository import TestRepository

class TestService:
    """
    SERVICE LAYER IS FOR HANDLING BUSINESS LOGIC.
    """
    def __init__(self):
        self.test_repository = TestRepository()
    
    async def fetch(self) -> str:
        message = await self.test_repository.fetch()
        return message


    