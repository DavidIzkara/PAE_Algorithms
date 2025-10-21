import vitaldb

class ShockIndex:
    def __init__(self, vf: vitaldb.VitalFile):
        # Get all available track names in the VitalFile
        available_tracks = vf.get_track_names()

        # Try to find heart rate and systolic pressure tracks
        hr_track = next(
            (t for t in available_tracks if 'Intellivue/ECG_HR' in t),          # First try for ECG_HR
            next((t for t in available_tracks if 'Intellivue/ABP_HR' in t),     # Then try for ABP_HR
                 next((t for t in available_tracks if 'Intellivue/HR' in t), None))) # Finally try for generic HR track
        sys_track = next(
            (t for t in available_tracks if 'Intellivue/ABP_SYS' in t), # First try for invasive systolic BP
            next((t for t in available_tracks if 'Intellivue/NIBP_SYS' in t), None)) # Then try for non-invasive systolic BP
        
        # Convert the signals to NumPy arrays
        hr = vf.to_numpy(track_names=hr_track)
        sys = vf.to_numpy(track_names=sys_track)

        # Computes the Shock Index (heart rate divided by systolic BP)
        self.values = hr / sys
#Handles both invasive and non-invasive blood pressure by checking available tracks.
#Requires heart rate track, tries multiple possible names for robustness.
#Does not require any special handling of missing data as this class is only used when we have the data.
