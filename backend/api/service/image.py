import uuid
from io import BytesIO
from pathlib import Path

from diffusers.utils.loading_utils import load_image
from fastapi import HTTPException, UploadFile
from PIL import Image

from api.clients import (
    CLIPClient,
    DiffusionClient,
    ImageMetadata,
    LocalStorageClient,
    QdrantClientManager,
    SQLiteClient,
)
from api.config import Settings
from api.schema import DeleteResponse, SimpleMetadata


class ImageService:
    def __init__(
        self,
        diffusion_client: DiffusionClient,
        clip_client: CLIPClient,
        qdrant_client: QdrantClientManager,
        sqlite_client: SQLiteClient,
        local_storage_client: LocalStorageClient,
        settings: Settings,
    ):
        self.diffusion_client: DiffusionClient = diffusion_client
        self.clip_client: CLIPClient = clip_client
        self.qdrant_client: QdrantClientManager = qdrant_client
        self.sqlite_client: SQLiteClient = sqlite_client
        self.local_storage_client: LocalStorageClient = local_storage_client
        self.settings = settings

    def generate_and_save_image(
        self,
        prompt: str,
        width: int,
        height: int,
        control_image_filename_1: str | None,
        control_image_filename_2: str | None,
        controlnet_conditioning_scale_1: float | None,
        controlnet_conditioning_scale_2: float | None,
        control_guidance_end_1: float | None,
        control_guidance_end_2: float | None,
        num_inference_steps: int,
        guidance_scale: float,
        seed: int,
    ) -> SimpleMetadata:
        """プロンプトから画像を生成し、embedding登録・ローカル保存・メタデータ保存を行う"""

        # 1. 引数から条件を構成する
        control_images: list[Image.Image] = []
        if (
            control_image_filename_1
            and Path(self.settings.CONDITION_IMAGE_DIR).exists()
        ):
            control_images.append(
                load_image(
                    str(
                        Path(self.settings.CONDITION_IMAGE_DIR)
                        / control_image_filename_1
                    )
                )
            )
        if (
            control_image_filename_2
            and Path(self.settings.CONDITION_IMAGE_DIR).exists()
        ):
            control_images.append(
                load_image(
                    str(
                        Path(self.settings.CONDITION_IMAGE_DIR)
                        / control_image_filename_2
                    )
                )
            )

        controlnet_conditioning_scale: list[float] = []
        if controlnet_conditioning_scale_1:
            controlnet_conditioning_scale.append(controlnet_conditioning_scale_1)
        if controlnet_conditioning_scale_2:
            controlnet_conditioning_scale.append(controlnet_conditioning_scale_2)

        control_guidance_end: list[float] = []
        if control_guidance_end_1:
            control_guidance_end.append(control_guidance_end_1)
        if control_guidance_end_2:
            control_guidance_end.append(control_guidance_end_2)

        ## サイズが同じか検証する
        if len(control_images) != len(controlnet_conditioning_scale):
            raise ValueError(
                "Control images and conditioning scales must match in length."
            )
        if len(control_images) != len(control_guidance_end):
            raise ValueError("Control images and guidance ends must match in length.")

        ## サイズが2以下であることを検証する
        if len(control_images) > 2:
            raise ValueError("Control images must be 0, 1, or 2 in length.")

        ## サイズが0の場合、ダミー画像を与える
        if not control_images:
            control_images = [Image.new("RGB", (width, height), (255, 255, 255))]
            controlnet_conditioning_scale = [0.0]
            control_guidance_end = [0.1]

        # 2. 画像生成
        image: Image.Image = self.diffusion_client.generate_image(
            prompt=prompt,
            control_images=control_images,
            width=width,
            height=height,
            controlnet_conditioning_scale=controlnet_conditioning_scale,
            control_guidance_end=control_guidance_end,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed,
        )

        # 3. 画像のembeddingとテキストのembeddingを生成
        image_embedding = self.clip_client.generate_image_embedding(image)
        text_embedding = self.clip_client.generate_text_embedding(prompt)

        # 4. 保存用ファイル名を決定
        image_filename = f"{uuid.uuid4().hex}.png"

        # 5. ローカルに画像保存 (ここでは省略。実際はちゃんと保存関数呼ぶ想定)
        self.local_storage_client.save_image(image, image_filename)

        # 6. Qdrantにアップロード
        self.qdrant_client.upload_point(
            image_embedding=image_embedding,
            text_embedding=text_embedding,
            image_filename=image_filename,
            prompt=prompt,
        )

        # 7. SQLiteにメタデータ保存
        self.sqlite_client.upload_metadata(
            image_filename=image_filename,
            prompt=prompt,
            width=width,
            height=height,
            control_image_filename_1=control_image_filename_1,
            control_image_filename_2=control_image_filename_2,
            controlnet_conditioning_scale_1=controlnet_conditioning_scale_1,
            controlnet_conditioning_scale_2=controlnet_conditioning_scale_2,
            control_guidance_end_1=control_guidance_end_1,
            control_guidance_end_2=control_guidance_end_2,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed,
        )

        # 8. レスポンス用の簡易メタデータを返す
        return SimpleMetadata(
            image_filename=image_filename,
            prompt=prompt,
        )

    def fetch_all_simple_metadata_list(self) -> list[SimpleMetadata]:
        """保存されている全ての画像についてシンプルなメタデータを取得"""
        retrieved_metadata_list: list[ImageMetadata] = (
            self.sqlite_client.retrieve_metadata_list()
        )
        simple_metadata_list = []
        for metadata in retrieved_metadata_list:
            simple_metadata = SimpleMetadata(
                image_filename=str(metadata.image_filename),
                prompt=str(metadata.prompt),
            )
            simple_metadata_list.append(simple_metadata)
        return simple_metadata_list

    async def search_similar_images(
        self,
        image: UploadFile | None = None,
        text: str | None = None,
        topk: int = 3,
    ) -> list[SimpleMetadata]:
        """テキストまたは画像に基づいて類似画像を検索する"""

        if not text and not image:
            raise ValueError("textまたはimageのどちらか一方は必須です。")

        # 埋め込み生成
        query_embedding = None
        if text:
            query_embedding = self.clip_client.generate_text_embedding(text)
        elif image:
            image_data = await image.read()
            pil_image = Image.open(BytesIO(image_data)).convert("RGB")
            query_embedding = self.clip_client.generate_image_embedding(pil_image)
        else:
            raise ValueError("textまたはimageのどちらか一方が必要です。")

        # Qdrantで検索
        simple_metadata_list: list[SimpleMetadata] = self.qdrant_client.search_points(
            query_embedding, topk=topk
        )

        return simple_metadata_list

    def delete_images(self, image_filenames: list[str]) -> DeleteResponse:
        """指定された画像ファイルを削除"""
        deleted_filenames = []
        failed_filenames = []

        for image_filename in image_filenames:
            try:
                self.qdrant_client.delete_point(image_filename)
                self.sqlite_client.delete_metadata(image_filename)
                self.local_storage_client.delete_image(image_filename)
                deleted_filenames.append(image_filename)
            except Exception as e:
                failed_filenames.append(image_filename)
                raise HTTPException(status_code=500, detail=str(e))

        return DeleteResponse(
            status="success" if not failed_filenames else "partial",
            deleted_filenames=deleted_filenames,
            failed_filenames=failed_filenames,
        )
