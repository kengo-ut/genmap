import pytest
from diffusers.utils.loading_utils import load_image
from PIL import Image

from api.clients import DiffusionClient
from tests.config import test_settings


@pytest.fixture
def diffusion_client():
    # テスト用のDiffusionクライアント
    client = DiffusionClient(test_settings)
    yield client


@pytest.fixture
def dummy_data():
    """テスト用のダミーデータを返す"""
    return {
        "prompt": "A girl waves her hands.",
        "control_images": [
            load_image(f"{test_settings.CONDITION_IMAGE_DIR}/sample.png")
        ],
        "width": 512,
        "height": 512,
        "controlnet_conditioning_scale": (0.5),
        "control_guidance_end": (0.8),
        "num_inference_steps": 5,
        "guidance_scale": 7.5,
        "seed": 42,
    }


def test_generate_image(diffusion_client, dummy_data):
    """画像が生成されるかテスト"""
    image = diffusion_client.generate_image(**dummy_data)

    assert isinstance(image, Image.Image)
