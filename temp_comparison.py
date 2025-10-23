import vitaldb

class TempComparison:
    def __init__(self, vf: vitaldb.VitalFile):

        available_tracks = vf.get_track_names()

        # Try to find core and skin temperature tracks
        core_track = next(
            (t for t in available_tracks if 'Intellivue/BT_CORE' in t), # First try for BT_CORE
            next((t for t in available_tracks if 'Intellivue/BT_BLD' in t), None)) # Then try for generic BT_BLD track
        skin_track = next(
            (t for t in available_tracks if 'Intellivue/BT_SKIN' in t), # First try for BT_SKIN
            next((t for t in available_tracks if 'Intellivue/TEMP' in t), None)) # Then try for generic TEMP track
        
        # Convert the signals to NumPy arrays
        core = vf.to_numpy(track_names=core_track)
        skin = vf.to_numpy(track_names=skin_track)

        # Store the results
        self.values = [core, skin]
