import vitaldb

class CardiacOutput:
    def __init__(self, vf: vitaldb.VitalFile):
         # Get all available track names in the VitalFile
        available_tracks = vf.get_track_names()

        # Try to find heart rate tracks
        hr_track = next(
            (t for t in available_tracks if 'Intellivue/ECG_HR' in t),          # First try for ECG_HR
            next((t for t in available_tracks if 'Intellivue/ABP_HR' in t),     # Then try for ABP_HR
                 next((t for t in available_tracks if 'Intellivue/HR' in t), None))) # Finally try for generic HR track
        
        self.values = vf.to_numpy(track_names = 'Intellivue/VOL_BLD_STROKE') * vf.to_numpy(track_names=hr_track)

#Calculates Cardiac Output by multiplying Stroke Volume by Heart Rate.
#Handles multiple possible heart rate track names for robustness.
