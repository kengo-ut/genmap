import shutil
from pathlib import Path

import pytest
from PIL import Image

from api.clients import LocalStorageClient
from tests.config import test_settings


@pytest.fixture
def local_storage_client():
    # テスト用のLocalStorageClient
    client = LocalStorageClient(test_settings)
    yield client
    if Path(test_settings.IMAGE_DIR).exists():
        shutil.rmtree(test_settings.IMAGE_DIR)


@pytest.fixture
def dummy_data():
    """テスト用のダミーデータを返す"""
    return {
        "image": Image.new("RGB", (512, 512), color="white"),  # 512x512の白い画像
        "image_filename": "test_image.png",
    }


def test_save_and_delete_image(local_storage_client, dummy_data):
    """画像が保存され、削除されるかテスト"""
    image_path = local_storage_client.save_image(**dummy_data)
    image = Image.open(image_path)
    assert isinstance(image, Image.Image)
    assert image.size == (512, 512)  # 予想される画像サイズ
    assert image.format == "PNG"  # 予想される画像フォーマット

    is_deleted = local_storage_client.delete_image(dummy_data["image_filename"])
    assert is_deleted
