import numpy as np
import pytest
from PIL import Image

from api.clients import CLIPClient
from tests.config import test_settings


@pytest.fixture
def clip_client():
    # テスト用のCLIPクライアント
    client = CLIPClient(test_settings)
    yield client


@pytest.fixture
def dummy_data():
    """テスト用のダミーデータを返す"""
    return Image.new("RGB", (224, 224), color="white")  # 224x224の白い画像


def test_generate_image_embedding(clip_client, dummy_data):
    """画像の埋め込みベクトルが生成されるかテスト"""
    embedding = clip_client.generate_image_embedding(dummy_data)
    assert embedding.shape == (512,)  # 予想される埋め込みベクトルの次元数
    assert np.allclose(
        np.linalg.norm(embedding), 1.0, atol=1e-6
    )  # 埋め込みベクトルの正規化


def test_generate_text_embedding(clip_client):
    """テキストの埋め込みベクトルが生成されるかテスト"""
    text = "A sample text"
    embedding = clip_client.generate_text_embedding(text)
    assert embedding.shape == (512,)  # 予想される埋め込みベクトルの次元数
    assert np.allclose(
        np.linalg.norm(embedding), 1.0, atol=1e-6
    )  # 埋め込みベクトルの正規化
