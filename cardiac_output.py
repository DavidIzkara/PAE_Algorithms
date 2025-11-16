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
        
        # Converts the signals to pandas dataframes
        hr = vf.to_pandas(track_names=hr_track, interval=0, return_timestamp=True)
        bld_track = 'Intellivue/VOL_BLD_STROKE'
        bld = vf.to_pandas(track_names=bld_track, interval=0, return_timestamp=True)

        
        # Deletes the nan values
        hr_clean = hr[hr[hr_track].notna()]
        bld_clean = bld[bld[bld_track].notna()]
        
        # Creates a new dataframe with timestamp | bld_value | bld_value where both values come from the same timestamp
        pre_co= bld_clean.merge(hr_clean, on="Time")

        #Creates the CO dataframe: Timestamp | CO_value
        self.values = {'Timestamp': pre_co["Time"], 'CO': pre_co[bld_track] * pre_co[hr_track]} 

#Calculates Cardiac Output by multiplying Stroke Volume by Heart Rate.
#Handles multiple possible heart rate track names for robustness.
