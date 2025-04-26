from fastapi import APIRouter, HTTPException, UploadFile

from api.schema import (
    DeleteResponse,
    ImageFilenames,
    ImageGenerationParams,
    SimpleMetadata,
)
from api.service import image_service

router = APIRouter(prefix="/image", tags=["image"])


@router.post("/generate", response_model=SimpleMetadata)
async def generate_image(request: ImageGenerationParams):
    """プロンプトから画像を生成し保存する"""
    try:
        result: SimpleMetadata = image_service.generate_and_save_image(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            control_image_filename_1=request.control_image_filename_1,
            control_image_filename_2=request.control_image_filename_2,
            controlnet_conditioning_scale_1=request.controlnet_conditioning_scale_1,
            controlnet_conditioning_scale_2=request.controlnet_conditioning_scale_2,
            control_guidance_end_1=request.control_guidance_end_1,
            control_guidance_end_2=request.control_guidance_end_2,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            seed=request.seed,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-simple-metadata", response_model=list[SimpleMetadata])
async def get_all_simple_metadata():
    """保存されている全ての画像についてシンプルなメタデータを取得する"""
    try:
        result: list[SimpleMetadata] = image_service.fetch_all_simple_metadata_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-control-image-filenames", response_model=list[str])
async def get_all_control_image_filenames():
    """control_imagesディレクトリにあるすべての画像ファイルについて名前を取得する"""
    try:
        result: list[str] = image_service.fetch_all_control_image_filenames()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=list[SimpleMetadata])
async def search_images(
    image: UploadFile | None = None,
    text: str | None = None,
    topk: int = 3,
):
    """テキストまたは画像に基づいて類似画像を検索する"""
    try:
        results: list[SimpleMetadata] = await image_service.search_similar_images(
            image=image, text=text, topk=topk
        )
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete", response_model=DeleteResponse)
async def delete_images(request: ImageFilenames):
    """画像を削除する"""
    try:
        result: DeleteResponse = image_service.delete_images(request.image_filenames)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
