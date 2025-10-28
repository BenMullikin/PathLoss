import numpy as np
from .base import PathLossModel

class WalfischIkegamiModel(PathLossModel):
    def __init__(self, f_0):
        super().__init__("Walfisch-Ikegami", f_0, baseHeight=None, receiverHeight=None)

    def predict(self, distance):
        return 42.6+26.*np.log10(distance)+20.*np.log10(self.f_0)