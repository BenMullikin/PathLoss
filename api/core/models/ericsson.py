import numpy as np
from .base import PathLossModel

class EricssonModel(PathLossModel):
    def __init__(self, f_0, baseHeight, receiverHeight, a0, a1, a2, a3):
        super().__init__("Ericsson", f_0, baseHeight, receiverHeight)
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def predict(self, distance):
        g = 44.49*np.log10(self.f_0) - 4.78*np.pow(np.log10(self.f_0),2)
        return self.a0 + self.a1*np.log10(distance)+self.a2*np.log10(self.baseHeight) + self.a3*np.log10(self.baseHeight)*np.log10(distance)-3.2*(np.log10(11.75*self.receiverHeight))**2 + g