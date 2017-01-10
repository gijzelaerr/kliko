from unittest import TestCase
from kliko import luigi_util


class TestLuigi(TestCase):
    def test_task(self):
        luigi_util.KlikoTask()

    def test_fileparameter(self):
        luigi_util.FileParameter()
