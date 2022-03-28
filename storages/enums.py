from enum import Enum


class StorageType(Enum):
    AWS_GLACIER = "glacier"
    AWS_S3 = "s3"
