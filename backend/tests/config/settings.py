from pathlib import Path

from api.config.settings import Settings


class TestSettings(Settings):
    # テスト用の設定だけ上書きする
    IMAGE_DIR: str = str(
        Path(__file__).resolve().parents[1] / "test_data" / "generated_images"
    )
    CONDITION_IMAGE_DIR: str = str(
        Path(__file__).resolve().parents[1] / "test_data" / "control_images"
    )
    SQLITE_DB_PATH: str = str(
        Path(__file__).resolve().parents[1] / "test_data" / "test_metadata.db"
    )
    QDRANT_DB_PATH: str = str(
        Path(__file__).resolve().parents[1] / "test_data" / "test_embeddings.db"
    )


# テスト用シングルトン
test_settings = TestSettings()
