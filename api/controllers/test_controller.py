from api.services.test_service import TestService
from api.utilities.app_response import AppResponse

class TestController:
    """
    CONTROLLER IS FOR HANDLING REQUEST AND RESPONSE.
    """

    def __init__(self):
        self.test_service = TestService()

    async def fetch(seft) -> str:
        message = await seft.test_service.fetch()
        return AppResponse.send_successful(
            data={
                "Message": message
            },
            message="Test Route Executed Successfully!"
        )