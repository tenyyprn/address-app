from PIL import Image
import os
import logging
from pathlib import Path
from typing import Optional, Tuple, Union
from src.app.config.settings import Settings

class ImageHandler:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif'}
        self.image_dir = Path(settings.image_storage_path)
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def load_image(self, file_path: Union[str, Path]) -> Optional[Image.Image]:
        try:
            file_path = Path(file_path)
            if not file_path.suffix.lower() in self.supported_formats:
                raise ValueError(f"Unsupported image format: {file_path.suffix}")
            return Image.open(file_path)
        except Exception as e:
            self.logger.error(f"Failed to load image {file_path}: {str(e)}")
            return None

    def save_image(self, image: Image.Image, file_path: Union[str, Path], quality: int = 85) -> bool:
        try:
            file_path = Path(file_path)
            image.save(file_path, quality=quality, optimize=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save image {file_path}: {str(e)}")
            return False

    def resize_image(self, image: Image.Image, size: Tuple[int, int], 
                    keep_aspect: bool = True) -> Optional[Image.Image]:
        try:
            if keep_aspect:
                image.thumbnail(size, Image.Resampling.LANCZOS)
                return image
            return image.resize(size, Image.Resampling.LANCZOS)
        except Exception as e:
            self.logger.error(f"Failed to resize image: {str(e)}")
            return None

    def create_thumbnail(self, image: Image.Image, max_size: Tuple[int, int] = (200, 200)) -> Optional[Image.Image]:
        try:
            thumbnail = image.copy()
            thumbnail.thumbnail(max_size, Image.Resampling.LANCZOS)
            return thumbnail
        except Exception as e:
            self.logger.error(f"Failed to create thumbnail: {str(e)}")
            return None

    def crop_image(self, image: Image.Image, box: Tuple[int, int, int, int]) -> Optional[Image.Image]:
        try:
            return image.crop(box)
        except Exception as e:
            self.logger.error(f"Failed to crop image: {str(e)}")
            return None

    def compress_image(self, image: Image.Image, quality: int = 85) -> Optional[Image.Image]:
        try:
            compressed = image.copy()
            compressed.save(self.image_dir / "temp.jpg", quality=quality, optimize=True)
            return Image.open(self.image_dir / "temp.jpg")
        except Exception as e:
            self.logger.error(f"Failed to compress image: {str(e)}")
            return None
        finally:
            if (self.image_dir / "temp.jpg").exists():
                (self.image_dir / "temp.jpg").unlink()

    def delete_image(self, file_path: Union[str, Path]) -> bool:
        try:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete image {file_path}: {str(e)}")
            return False

    def validate_image(self, file_path: Union[str, Path]) -> bool:
        try:
            file_path = Path(file_path)
            if not file_path.suffix.lower() in self.supported_formats:
                return False
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def get_image_info(self, image: Image.Image) -> dict:
        return {
            'format': image.format,
            'size': image.size,
            'mode': image.mode,
            'info': image.info
        }