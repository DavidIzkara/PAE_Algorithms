import vitaldb
from vitaldb import VitalFile
import os

from shock_index import ShockIndex
from driving_pressure import DrivingPressure
from dynamic_compliance import DynamicCompliance
from rox_index import RoxIndex
from temp_comparison import TempComparison
#from cardiac_output import CardiacOutput
#from systemic_vascular_resistance import SystemicVascularResistance
#from cardiac_power_output import CardiacPowerOutput
#from effective_arterial_elastance import EffectiveArterialElastance

def key_datetime(fname):
    base = os.path.splitext(os.path.basename(fname))[0]
    parts = base.split('_')
    return parts[-2] + parts[-1]

def find_latest_vital(recordings_dir):
    if not os.path.isdir(recordings_dir):
        return None

    # Numeric subfolders
    folders = [d for d in os.listdir(recordings_dir)
               if os.path.isdir(os.path.join(recordings_dir, d)) and d.isdigit()]
    if not folders:
        return None

    latest_folder = sorted(folders)[-1]
    folder_path = os.path.join(recordings_dir, latest_folder)

    # Latest .vital file
    vitals = [f for f in os.listdir(folder_path) if f.endswith('.vital')]
    if not vitals:
        return None

    latest = sorted(vitals, key=key_datetime)[-1]
    return os.path.join(folder_path, latest)

selected_list = []

def check_availability(tracks): #Función que comprueba qué algoritmos se pueden calcular con las variables disponibles.
    possible_list = []

    if ('Intellivue/ECG_HR' in tracks or 'Intellivue/ABP_HR' in tracks or 'Intellivue/HR' in tracks) and ('Intellivue/ABP_SYS' in tracks or 'Intellivue/BP_SYS' in tracks or 'Intellivue/NIBP_SYS' in tracks):
        possible_list.append('Shock Index')
    if 'Intellivue/PPLAT_CMH2O' in tracks and 'Intellivue/PEEP_CMH2O' in tracks:
        possible_list.append('Driving Pressure')
    if 'Intellivue/TV_EXP' in tracks and 'Intellivue/PIP_CMH2O' in tracks and 'Intellivue/PEEP_CMH2O' in tracks:
        possible_list.append('Dynamic Compliance')
    if 'Intellivue/PLETH_SAT_O2' in tracks and 'Intellivue/FiO2' in tracks:
        possible_list.append('ROX Index')
    if ('Intellivue/BT_CORE' in tracks or 'Intellivue/BT_BLD' in tracks) and ('Intellivue/BT_SKIN' in tracks or 'Intellivue/TEMP' in tracks):
        possible_list.append('Temp Comparison')
    #Variables MostCare
    if 'Intellivue/VOL_BLD_STROKE' in tracks and ('Intellivue/ECG_HR' in tracks or 'Intellivue/ABP_HR' in tracks or 'Intellivue/HR' in tracks):
        possible_list.append('Cardiac Output')
    if ('Intellivue/ABP_MEAN' in tracks or 'Intellivue/BP_MEAN' in tracks or 'Intellivue/NIBP_MEAN' in tracks) and 'Intellivue/CVP_MEAN' in tracks and 'Cardiac Output' in possible_list:
        possible_list.append('Systemic Vascular Resistance')
    if ('Intellivue/ABP_MEAN' in tracks or 'Intellivue/BP_MEAN' in tracks or 'Intellivue/NIBP_MEAN' in tracks) and 'Cardiac Output' in possible_list:
        possible_list.append('Cardiac Power Output')
    if ('Intellivue/ABP_SYS' in tracks or 'Intellivue/BP_SYS' in tracks or 'Intellivue/NIBP_SYS' in tracks) and 'Intellivue/VOL_BLD_STROKE' in tracks:
        possible_list.append('Effective Arterial Elastance')
    #Ver si se pueden añadir más variables MostCare

    #Pendiente Comprobar Variables autonomicas

    if 'Intellivue/ICP' in tracks: #Might need more variables
        possible_list.append('ICP Model')
    if 'Intellivue/PLETH' in tracks and 'Intellivue/ART' in tracks and 'Intellivue/ABP' in tracks:
        possible_list.append('ABP Model')
    
    #Pendiente Comprobar otros algoritmos

    return possible_list #Esta lista se envía al front para que el usuario seleccione.


recordings_dir = ##Pon la carpeta donde tengas el .vital, recomendado poner: r"\path"
vital_path = find_latest_vital(recordings_dir)
vf = VitalFile(vital_path)

tracks = vf.get_track_names()
print("Track names: ", tracks)
print("Los algoritmos disponibles son: ", check_availability(tracks))

results = {}
results['Shock Index'] = ShockIndex(vf).values
results['Driving Pressure'] = DrivingPressure(vf).values
results['Dynamic Compliance'] = DynamicCompliance(vf).values
#results['ROX Index'] = RoxIndex(vf).values
#results['Temp Comparison'] = TempComparison(vf).values
#results['Cardiac Output'] = CardiacOutput(vf).values
#results['Systemic Vascular Resistance'] = SystemicVascularResistance(vf).values
#results['Cardiac Power Output'] = CardiacPowerOutput(vf).values
#results['Effective Arterial Elastance'] = EffectiveArterialElastance(vf).values

#Print results to verify
print("DP: ", results['Driving Pressure'])
