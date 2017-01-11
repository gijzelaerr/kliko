from unittest import TestCase
from kliko import luigi_util


class TestLuigi(TestCase):
    def test_task(self):

        class TestKlikoTask(luigi_util.KlikoTask):
            @classmethod
            def image_name(cls):
                return "kliko/minimal"

        TestKlikoTask(file='test', int=10)

    def test_fileparameter(self):
        luigi_util.FileParameter()
