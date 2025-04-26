from pathlib import Path

import torch
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DEVICE: str = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    EMBEDDING_DIM: int = 512

    # データベース
    IMAGE_DIR: str = str(
        Path(__file__).resolve().parents[1] / "data" / "generated_images"
    )
    CONDITION_IMAGE_DIR: str = str(
        Path(__file__).resolve().parents[1] / "data" / "control_images"
    )
    SQLITE_DB_PATH: str = str(
        Path(__file__).resolve().parents[1] / "data" / "metadata.db"
    )
    QDRANT_DB_PATH: str = str(
        Path(__file__).resolve().parents[1] / "data" / "embeddings.db"
    )
    COLLECTION_NAME: str = "image_embeddings"

    # モデル
    SD_BASE_MODEL: str = "black-forest-labs/FLUX.1-dev"  # Stable Diffusion ベースモデル
    CONTROLNET_MODEL: str = (
        "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0"  # ControlNet モデル
    )

    CLIP_EMBEDDING_MODEL: str = (
        "openai/clip-vit-base-patch32"  # 画像・テキスト埋め込み用のCLIPモデル
    )


# シングルトンとして設定をエクスポート
settings = Settings()
