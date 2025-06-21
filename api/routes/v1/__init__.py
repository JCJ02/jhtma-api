from fastapi import APIRouter
from api.routes.v1.test_route import router as test_router
from api.routes.v1.users_route import router as users_router
from api.routes.v1.roles_route import router as roles_router

router = APIRouter(prefix="/api/v1")

router.include_router(test_router, prefix="/test", tags=["Test"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(roles_router, prefix="/roles", tags=["Roles"])
