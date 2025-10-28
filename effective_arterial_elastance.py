import vitaldb

class EffectiveArterialElastance:
    def __init__(self, vf: vitaldb.VitalFile):
        # Get all available track names in the VitalFile
        available_tracks = vf.get_track_names()

        # Try to find systolic pressure tracks
        sys_track = next(
            (t for t in available_tracks if 'Intellivue/ABP_SYS' in t), # First try for invasive systolic BP
            next((t for t in available_tracks if 'Intellivue/BP_SYS' in t), # Then try for another possible invasive systolic BP
                next((t for t in available_tracks if 'Intellivue/NIBP_SYS' in t), None))) # Finally try for non-invasive systolic BP
        

        #  0.9 × SBP(systolic Blood Presure) / SV (Stroke Volume)
        self.values = (0.9 * vf.to_numpy(track_names = sys_track)) / vf.to_numpy(track_names = 'Intellivue/VOL_BLD_STROKE')
