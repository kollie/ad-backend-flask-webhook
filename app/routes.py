from fastapi import APIRouter
from app.resources import user, food, result

router = APIRouter()

# User routes
router.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
)

# Food routes
router.include_router(
    food.router,
    prefix="/foods",
    tags=["foods"]
)

# Result routes
router.include_router(
    result.router,
    prefix="/results",
    tags=["results"]
)





