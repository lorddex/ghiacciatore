# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
