import vitaldb
from cardiac_output import CardiacOutput

class CardiacPowerOutput:
    def __init__(self, vf: vitaldb.VitalFile):
        # Get all available track names in the VitalFile
        available_tracks = vf.get_track_names()

        # Try to find mean pressure tracks
        mean_track = next(
            (t for t in available_tracks if 'Intellivue/ABP_MEAN' in t), # First try for invasive mean BP
            next((t for t in available_tracks if 'Intellivue/BP_MEAN' in t), # Then try for another possible invasive mean BP
                next((t for t in available_tracks if 'Intellivue/NIBP_MEAN' in t), None))) # Finally try for non-invasive mean BP
        
        self.values = (vf.to_numpy(track_names = mean_track) * CardiacOutput(vf).values) / 451.0

#Calculates Cardiac Power Output by multiplying Mean Arterial Pressure by Cardiac Output and dividing by 451.
#Handles multiple possible mean pressure track names for robustness.
