from kliko.luigi_util import KlikoTask


class SimmsTask(KlikoTask):
    @classmethod
    def imagename(cls):
        return "kliko/simms"

