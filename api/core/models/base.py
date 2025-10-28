from abc import ABC, abstractmethod
import numpy as np

class PathLossModel(ABC):
    def __init__(self, name, f_0, baseHeight, receiverHeight):
        self.name = name
        self.f_0 = f_0
        self.baseHeight = baseHeight
        self.receiverHeight = receiverHeight

    @abstractmethod
    def predict(self, distance: np.ndarray) -> np.ndarray:
        """
        Predict the pathloss in dB for a all distances in distance 

        :param distance: An array of distances in km.
        :type distance: np.ndarray
        :returns: np.ndarray of pathloss in dB
        :rtype: np.ndarray
        """
        pass

    def evaluate_rmse(self, distance: np.ndarray, measured: list) -> float:
        """
        This function returns the rmse of the predicted values vs measured

        :param distance: An array of distances in km.
        :type distance: np.ndarray
        :param measured: A list of measured values in km.
        :type measured: list
        :returns: The measured RMSE
        :rtype: float
        """
        predicted = self.predict(distance)
        return np.sqrt(np.mean((np.asarray(measured) - np.asarray(predicted))**2))