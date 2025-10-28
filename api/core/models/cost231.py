import numpy as np
from .base import PathLossModel

class Cost231Model(PathLossModel):
    def __init__(self, f_0, baseHeight, receiverHeight, enviroment):
        super().__init__("Cost 231", f_0, baseHeight, receiverHeight)
        self.enviroment = enviroment

    def predict(self, distance):
        if self.enviroment == "urban":
            ah_m = 3.2*(np.log10(11.75*self.receiverHeight))*2 - 4.97
            C_m = 3
        elif self.enviroment == "suburban" or self.enviroment == "rural":
            ah_m = (1.1*np.log10(self.f_0)*self.receiverHeight) - 1.56*np.log10(self.receiverHeight-0.8)
            C_m = 0
        else: 
            raise ValueError("Invalid enivorment. Please select rural, suburban, urban")
        return 46.3 + 33.9*np.log10(self.f_0)-13.82*np.log10(self.baseHeight) - ah_m + (44.9-6.55*np.log10(self.baseHeight))*np.log10(distance) + C_m