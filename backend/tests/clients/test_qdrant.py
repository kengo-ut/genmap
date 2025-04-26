import shutil
from pathlib import Path

import numpy as np
import pytest

from api.clients.qdrant import QdrantClientManager
from api.schema import SimpleMetadata
from tests.config import test_settings


@pytest.fixture
def qdrant_manager():
    # 初期化
    manager = QdrantClientManager(test_settings)
    yield manager

    # テスト後にデータベース削除
    if Path(test_settings.QDRANT_DB_PATH).exists:
        shutil.rmtree(test_settings.QDRANT_DB_PATH)


@pytest.fixture
def dummy_data():
    """テスト用のダミーデータを返す"""
    return {
        "image_filename": "test.png",
        "prompt": "A test image",
        "embedding": np.random.rand(test_settings.EMBEDDING_DIM),
    }


def test_upload_and_search_point(qdrant_manager, dummy_data):
    manager = qdrant_manager
    image_filename = dummy_data["image_filename"]
    prompt = dummy_data["prompt"]
    embedding = dummy_data["embedding"]

    # アップロード
    manager.upload_point(
        image_embedding=embedding,
        text_embedding=embedding,
        image_filename=image_filename,
        prompt=prompt,
    )

    # 検索
    results = manager.search_points(query_embedding=embedding, topk=1)
    assert len(results) == 1
    result = results[0]
    assert isinstance(result, SimpleMetadata)
    assert result.image_filename == image_filename
    assert result.prompt == prompt


def test_delete_point(qdrant_manager, dummy_data):
    manager = qdrant_manager
    image_filename = dummy_data["image_filename"]
    prompt = dummy_data["prompt"]
    embedding = dummy_data["embedding"]

    # アップロード
    manager.upload_point(
        image_embedding=embedding,
        text_embedding=embedding,
        image_filename=image_filename,
        prompt=prompt,
    )

    # 削除前に検索して存在確認
    results = manager.search_points(query_embedding=embedding, topk=1)
    assert results[0].image_filename == image_filename

    # 削除
    manager.delete_point(image_filename=image_filename)

    # 削除後の確認
    results = manager.search_points(query_embedding=embedding, topk=1)
    assert len(results) == 0
