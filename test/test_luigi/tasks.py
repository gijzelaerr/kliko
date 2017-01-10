from kliko.luigi_util import KlikoTask
import luigi


class LuigiTest1(KlikoTask):
    @classmethod
    def image_name(cls):
        return "kliko/luigitest1:0.1"


class LuigiTest2(KlikoTask):
    @classmethod
    def image_name(cls):
        return "kliko/luigitest2:0.1"

    def requires(self):
        return LuigiTest1()


class LuigiTest3(KlikoTask):
    @classmethod
    def image_name(cls):
        return "kliko/luigitest3:0.1"

    def requires(self):
        return LuigiTest2()
