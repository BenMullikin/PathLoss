import numpy as np
from .base import PathLossModel

class ECC33Model(PathLossModel):
    def __init__(self, f_0):
        super().__init__("ECC 33", f_0)

    def predict(self, distance):
        return 32.45 + 20*np.log10(distance) + 20*np.log(self.f_0) # This is pulled from provided matlab code