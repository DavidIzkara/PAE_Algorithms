import vitaldb
from cardiac_output import CardiacOutput

class SystemicVascularResistance:
    def __init__(self, vf: vitaldb.VitalFile):
        # Get all available track names in the VitalFile
        available_tracks = vf.get_track_names()

        # Try to find systolic pressure tracks
        sys_track = next(
            (t for t in available_tracks if 'Intellivue/ABP_MEAN' in t), # First try for invasive systolic BP
            next((t for t in available_tracks if 'Intellivue/NIBP_MEAN' in t), None)) # Then try for non-invasive systolic BP
        
        self.vf = ((vf.to_numpy(track_names = sys_track) - vf.to_numpy(track_names = 'Intellivue/CVP_MEAN')) * 80) / CardiacOutput(vf).values

#Calculates Systemic Vascular Resistance using Mean Arterial Pressure, Central Venous Pressure, and Cardiac Output.
#Handles multiple possible mean arterial pressure track names for robustness.
