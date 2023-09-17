import io
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.files.base import File
from PIL import Image as PILImage

from common.utils import image_s3_upload


def create_sample_image():
    image = PILImage.new("RGB", (100, 100))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_data = image_bytes.getvalue()
    image_file = io.BytesIO(image_data)
    image_file.name = "test_image.jpg"
    image_file = File(image_file)
    return image_file


class ImageS3UploadTestCase(TestCase):
    @patch("common.utils.Image.s3_client")
    def test_image_s3_upload(self, s3_client: MagicMock):
        s3_client.upload_fileobj.return_value = None
        s3_client.put_object_acl.return_value = None

        sample_image = create_sample_image()
        validated_data = {"image": sample_image}
        result = image_s3_upload(validated_data, "test")

        self.assertTrue(
            result.get("image_url").startswith("https://kr.object.ncloudstorage.com")
        )

        s3_client.upload_fileobj.assert_called_once()
        s3_client.put_object_acl.assert_called_once()
