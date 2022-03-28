from enum import Enum
from typing import TypeVar

Self = TypeVar("Self", bound="StorageType")


class StorageType(Enum):
    AWS_GLACIER = "glacier"
    AWS_S3 = "s3"

    @staticmethod
    def value_of(value: str) -> Self:
        for name, member in StorageType.__members__.items():
            if member.value == value:
                return member
