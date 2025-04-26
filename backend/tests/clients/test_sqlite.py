import os
from pathlib import Path

import pytest

from api.clients import SQLiteClient
from tests.config import test_settings


@pytest.fixture
def sql_client():
    # テスト用のSQLiteクライアント
    client = SQLiteClient(test_settings)
    yield client
    # テスト後にDBを削除する
    if Path(test_settings.SQLITE_DB_PATH).exists:
        os.remove(test_settings.SQLITE_DB_PATH)


@pytest.fixture
def dummy_data():
    """テスト用のダミーデータを返す"""
    return {
        "image_filename": "test.png",
        "prompt": "A test image",
        "width": 512,
        "height": 512,
        "control_image_filename_1": "cond1.png",
        "control_image_filename_2": "cond2.png",
        "controlnet_conditioning_scale_1": 0.5,
        "controlnet_conditioning_scale_2": 0.6,
        "control_guidance_end_1": 0.8,
        "control_guidance_end_2": 0.9,
        "num_inference_steps": 30,
        "guidance_scale": 7.5,
        "seed": 42,
    }


def test_upload_metadata(sql_client, dummy_data):
    client = sql_client

    # メタデータをアップロード
    uploaded_metadata = client.upload_metadata(**dummy_data)

    # アップロードしたデータの検証
    assert uploaded_metadata.image_filename == dummy_data["image_filename"]
    assert uploaded_metadata.prompt == dummy_data["prompt"]
    assert (
        uploaded_metadata.control_image_filename_1
        == dummy_data["control_image_filename_1"]
    )
    assert (
        uploaded_metadata.control_image_filename_2
        == dummy_data["control_image_filename_2"]
    )
    assert (
        uploaded_metadata.controlnet_conditioning_scale_1
        == dummy_data["controlnet_conditioning_scale_1"]
    )
    assert (
        uploaded_metadata.controlnet_conditioning_scale_2
        == dummy_data["controlnet_conditioning_scale_2"]
    )
    assert (
        uploaded_metadata.control_guidance_end_1 == dummy_data["control_guidance_end_1"]
    )
    assert (
        uploaded_metadata.control_guidance_end_2 == dummy_data["control_guidance_end_2"]
    )
    assert uploaded_metadata.num_inference_steps == dummy_data["num_inference_steps"]
    assert uploaded_metadata.guidance_scale == dummy_data["guidance_scale"]
    assert uploaded_metadata.seed == dummy_data["seed"]


def test_retrieve_metadata(sql_client, dummy_data):
    client = sql_client

    # ダミーデータをアップロード
    client.upload_metadata(**dummy_data)

    # メタデータを取得
    retrieved_metadata_list = client.retrieve_metadata_list()

    # 取得したデータの検証
    assert len(retrieved_metadata_list) == 1
    retrieved_metadata = retrieved_metadata_list[0]
    assert retrieved_metadata.image_filename == dummy_data["image_filename"]
    assert retrieved_metadata.prompt == dummy_data["prompt"]
    assert (
        retrieved_metadata.control_image_filename_1
        == dummy_data["control_image_filename_1"]
    )
    assert (
        retrieved_metadata.control_image_filename_2
        == dummy_data["control_image_filename_2"]
    )
    assert (
        retrieved_metadata.controlnet_conditioning_scale_1
        == dummy_data["controlnet_conditioning_scale_1"]
    )
    assert (
        retrieved_metadata.controlnet_conditioning_scale_2
        == dummy_data["controlnet_conditioning_scale_2"]
    )
    assert (
        retrieved_metadata.control_guidance_end_1
        == dummy_data["control_guidance_end_1"]
    )
    assert (
        retrieved_metadata.control_guidance_end_2
        == dummy_data["control_guidance_end_2"]
    )
    assert retrieved_metadata.num_inference_steps == dummy_data["num_inference_steps"]
    assert retrieved_metadata.guidance_scale == dummy_data["guidance_scale"]
    assert retrieved_metadata.seed == dummy_data["seed"]


def test_delete_metadata(sql_client, dummy_data):
    client = sql_client

    # ダミーデータをアップロード
    client.upload_metadata(**dummy_data)

    # データ削除前に存在を確認
    retrieved_metadata_list_before = client.retrieve_metadata_list()
    assert len(retrieved_metadata_list_before) == 1

    # メタデータを削除
    client.delete_metadata(dummy_data["image_filename"])

    # データ削除後に確認
    retrieved_metadata_list_after = client.retrieve_metadata_list()
    assert len(retrieved_metadata_list_after) == 0
