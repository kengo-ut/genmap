from fastapi import APIRouter

from .image import router as image_router

# メインルーターの作成と各サブルーターの登録
router = APIRouter()
router.include_router(image_router)

__all__ = ["router"]
