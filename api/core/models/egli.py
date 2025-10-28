import numpy as np
from .base import PathLossModel

class EGLIModel(PathLossModel):
    def __init__(self, f_0, baseHeight, receiverHeight):
        super().__init__("EGLI", f_0, baseHeight, receiverHeight)

    def predict(self, distance):
        if self.receiverHeight < 0.01:
            L_m = 76.3 - 10*np.log10(self.receiverHeight)
        else:
            L_m = 85.9 - 20*np.log10(self.receiverHeight)
        return 40*np.log10(distance) + 20*np.log10(self.f_0) - 20*np.log10(self.baseHeight) + L_m