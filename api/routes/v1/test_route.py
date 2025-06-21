from fastapi import APIRouter
from api.controllers.test_controller import TestController

router = APIRouter()

test_controller = TestController()

@router.get("/")
async def test_route():
    """
    ROUTES IS FOR API ENDPOINTS OF APIs
    """
    return await test_controller.fetch()