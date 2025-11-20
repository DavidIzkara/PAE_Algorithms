import vitaldb
import numpy as np
from funcion_RR import funcion_rr


class HeartRateVariability:

    def __init__(self, vf: vitaldb.VitalFile):
        # Convert the signals to NumPy arrays
        hr = vf.to_pandas(track_names="Intellivue/ECG_II", interval=0)
        rr = funcion_rr(vf)
        print("Valores rr?:", rr)

        # Calculate HRV metrics
        sdnn = self.compute_sdnn(rr)
        rmssd = self.compute_rmssd(rr)
        pnn50 = self.compute_pnn50(rr)

    def compute_sdnn(self, rr, window=5):
        n = len(rr)
        result = []
        for i in range(n - window + 1):
            w = rr[i : i + window]
            result.append(np.std(w, ddof=1))
        return np.array(result)

    def compute_rmssd(self, rr, window=5):
        n = len(rr)
        result = []
        for i in range(n - window + 1):
            w = rr[i : i + window]
            diffs = np.diff(w)
            result.append(np.sqrt(np.mean(diffs ** 2)))
        return np.array(result)

    def compute_pnn50(self, rr, window=5, threshold=50):
        n = len(rr)
        result = []
        for i in range(n - window + 1):
            w = rr[i : i + window]
            diffs = np.abs(np.diff(w))
            count = np.sum(diffs > threshold)
            result.append(count / (len(diffs)) * 100)
        return np.array(result)

    
