import uuid
from datetime import datetime

from django.conf import settings
from django.core.files.base import File

from boto3 import client


class Image:
    def __init__(self, image: File):
        self.file = image.file
        self.name = image.name
        self.id = str(uuid.uuid4())
        self.ext = self.name.split(".")[-1]
        self.directory = datetime.now().date()
        self.filename = f"MEDIA/profile/{self.directory}/{self.id}.{self.ext}"
        self.url = None
        self.access_key = settings.NCP_ACCESS_KEY
        self.secret_key = settings.NCP_SECRET_KEY
        self.endpoint_url = settings.NCP_S3_ENDPOINT_URL
        self.bucket_name = settings.NCP_S3_BUCKET_NAME
        self.client: client = client(
            service_name="s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def s3_upload(self):
        try:
            self.client.upload_fileobj(self.file, self.bucket_name, self.filename)
            self.url = f"{self.endpoint_url}/{self.bucket_name}/{self.filename}"
            print("Upload the Image Successfully")
        except Exception as e:
            print(f"Image upload failed: {e}")

    def set_public_in_s3(self):
        try:
            response = self.client.put_object_acl(
                Bucket=self.bucket_name, Key=self.filename, ACL="public-read"
            )
            print("Set the Image to Public Successfully")
        except Exception as e:
            print(f"Image setting to public failed: {e}")


def image_s3_upload(validated_data):
    if "image" in validated_data:
        image_file = validated_data.pop("image")
        image = Image(image_file)
        image.s3_upload()
        image.set_public_in_s3()
        validated_data["image_url"] = image.url
    return validated_data
