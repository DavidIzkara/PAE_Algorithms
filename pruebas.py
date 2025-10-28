import vitaldb 
from vitaldb import VitalFile

from shock_index import ShockIndex
from driving_pressure import DrivingPressure
from dynamic_compliance import DynamicCompliance
from rox_index import RoxIndex
from temp_comparison import TempComparison
from cardiac_output import CardiacOutput
from systemic_vascular_resistance import SystemicVascularResistance
from cardiac_power_output import CardiacPowerOutput
from effective_arterial_elastance import EffectiveArterialElastance

vital_path = find_latest_vital(recordings_dir) #Función que encuentra el último fichero de vital.
vf = VitalFile(vital_path)

results = {}    
results['Shock Index'] = ShockIndex(vf).values
results['Driving Pressure'] = DrivingPressure(vf).values    
#results['Dynamic Compliance'] = DynamicCompliance(vf).values
results['ROX Index'] = RoxIndex(vf).values
results['Temp Comparison'] = TempComparison(vf).values
#results['Cardiac Output'] = CardiacOutput(vf).values
#results['Systemic Vascular Resistance'] = SystemicVascularResistance(vf).values
#results['Cardiac Power Output'] = CardiacPowerOutput(vf).values
#results['Effective Arterial Elastance'] = EffectiveArterialElastance(vf).values
#Pasar los resultados a un .csv
import pandas as pd
df = pd.DataFrame(results)
df.to_csv('resultados_algoritmos.csv', index=False)
