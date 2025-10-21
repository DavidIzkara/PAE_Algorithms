import vitaldb

class DrivingPressure:
    def __init__(self, vf: vitaldb.VitalFile):
        self.values = vf.to_numpy(track_names = 'Intellivue/PPLAT_CMH2O') - vf.to_numpy(track_names = 'Intellivue/PEEP_CMH2O')
#Does the driving pressure calculation by subtracting PEEP from PLAT.
#Does not require any special handling of missing data as this class is only used when we have the data.
#Does not need to handle multiple possible track names as these are fixed.
