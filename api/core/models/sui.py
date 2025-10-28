import numpy as np
from .base import PathLossModel

class SUIModel(PathLossModel):
    def __init__(self, f_0, baseHeight, receiverHeight, terrain_a, terrain_b, terrain_c, shadowFading, d_0):
        super().__init__("SUI", f_0, baseHeight, receiverHeight)
        self.terrain_a = terrain_a
        self.terrain_b = terrain_b
        self.terrain_c = terrain_c
        self.shadowFading = shadowFading
        self.d_0 = d_0

    def predict(self, distance):
        c = 3e8
        wavelength = c / (self.f_0 * 1e6)
        gamma = self.terrain_a - self.terrain_b * self.baseHeight + self.terrain_c / self.baseHeight

        A = 20*np.log10((4*np.pi*self.d_0*1e3) / wavelength)
        X_f = 6*np.log10((self.f_0)/2000)
        if self.terrain_c == 20:
            X_h = -20*np.log10(self.receiverHeight/2000)
        else: 
            X_h = -10.8*np.log10(self.receiverHeight/2000)
        return A + 10*gamma*np.log10(distance/self.d_0) + X_f + X_h + self.shadowFading - 10