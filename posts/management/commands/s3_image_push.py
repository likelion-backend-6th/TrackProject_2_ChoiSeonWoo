from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand

from common.utils import Image


# TODO: 커맨드 활용
# https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/#testing
class Command(BaseCommand):
    help = "Upload Image to S3 and Check ImageURL"

    def handle(self, *args, **options):
        test_file_path = settings.BASE_DIR / "media/s3.png"

        with open(test_file_path, "rb") as buffered_file:
            image_file = File(buffered_file)
            image = Image(image_file)
            image.s3_upload()
            image.set_public_in_s3()
