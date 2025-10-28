import vitaldb

class DynamicCompliance:
    def __init__(self, vf: vitaldb.VitalFile): #Falta ver el nombre correcto de la variable de volumen tidal
        self.values = vf.to_numpy(track_names = 'Intellivue/TV_EXP') / (vf.to_numpy(track_names = 'Intellivue/PIP_CMH2O') - vf.to_numpy(track_names = 'Intellivue/PEEP_CMH2O'))
#Does the compliance calculation by subtracting driving pressure from tidal volume.
#Does not require any special handling of missing data as this class is only used when we have the data.
#Does not need to handle multiple possible track names as these are fixed.
