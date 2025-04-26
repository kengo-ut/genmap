from pathlib import Path

from PIL import Image

from api.config import Settings


class LocalStorageClient:
    def __init__(self, settings: Settings):
        self.image_dir = settings.IMAGE_DIR
        self.control_image_dir = settings.CONDITION_IMAGE_DIR
        Path(self.image_dir).mkdir(parents=True, exist_ok=True)
        Path(self.control_image_dir).mkdir(parents=True, exist_ok=True)

    def save_image(self, image: Image.Image, image_filename: str) -> Path:
        """画像をローカルに保存"""
        image_path = Path(self.image_dir) / image_filename
        image.save(image_path)
        return image_path

    def delete_image(self, image_filename: str) -> bool:
        """ローカルの画像を削除"""
        image_path = Path(self.image_dir) / image_filename
        if image_path.exists():
            image_path.unlink()
            return True
        return False
