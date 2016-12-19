from kliko.luigi_util import KlikoTask


class SimmsTask(KlikoTask):
    @classmethod
    def image_name(cls):
        return "kliko/simms"

