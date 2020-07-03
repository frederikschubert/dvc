# pylint:disable=abstract-method
import os
import uuid

import pytest

from dvc.path_info import CloudURLInfo
from dvc.utils import env2bool

from .base import Base

TEST_OSS_REPO_BUCKET = "dvc-test"


class OSS(Base, CloudURLInfo):
    @staticmethod
    def should_test():
        do_test = env2bool("DVC_TEST_OSS", undefined=None)
        if do_test is not None:
            return do_test

        return (
            os.getenv("OSS_ENDPOINT")
            and os.getenv("OSS_ACCESS_KEY_ID")
            and os.getenv("OSS_ACCESS_KEY_SECRET")
        )

    @staticmethod
    def _get_storagepath():
        return f"{TEST_OSS_REPO_BUCKET}/{uuid.uuid4()}"

    @staticmethod
    def get_url():
        return f"oss://{OSS._get_storagepath()}"


@pytest.fixture
def oss():
    if not OSS.should_test():
        pytest.skip("no oss running")
    yield OSS(OSS.get_url())
