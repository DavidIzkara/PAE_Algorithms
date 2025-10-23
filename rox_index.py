import vitaldb

class RoxIndex:
    def __init__(self, vf: vitaldb.VitalFile):
        self.values = vf.to_numpy(track_names = 'Intellivue/PLETH_SAT_O2') / vf.to_numpy(track_names = 'Intellivue/FiO2')
#Does the ROX index calculation by dividing oxygen saturation by FiO2.
#Does not require any special handling of missing data as this class is only used when we have the data.
#Does not need to handle multiple possible track names as these are fixed.
