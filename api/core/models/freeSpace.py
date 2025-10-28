import numpy as np
from .base import PathLossModel

class FreeSpaceModel(PathLossModel):
    def __init__(self, f_0):
        super().__init__("Free Space", f_0, baseHeight=None, receiverHeight=None)

    def predict(self, distance):
        return 32.45 + 20.*np.log10(distance) + 20.*np.log10(self.f_0)