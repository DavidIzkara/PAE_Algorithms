import vitaldb 
from vitaldb import VitalFile

from shock_index import ShockIndex
from driving_pressure import DrivingPressure
from compliance import Compliance
from rox_index import RoxIndex
from temp_comparison import TempComparison
#Pendiente importar ICP Model


#Este código va en back-end, las definiciones de las variables ya están hechas, es solo para ver cómo se usa la clase.:

vital_path = find_latest_vital(recordings_dir) #Función que encuentra el último fichero de vital.
vf = VitalFile(vital_path) # Aquí esta todo el fichero.
tracks = vf.get_track_names() #Aquí están todos los nombres de las variables.
raw = vf.to_numpy(tracks, interval=0, return_timestamp=True) #Aquí están todos los datos en bruto.

selected_list = []

def check_availability(tracks): #Función que comprueba qué algoritmos se pueden calcular con las variables disponibles.
    possible_list = []

    if 'Intellivue/ECG_HR' and ('Intellivue/ABP_SYS' or 'Intellivue/NIBP_SYS') in tracks:
        possible_list.append('Shock Index')
    if 'Intellivue/PPLAT_CMH2O' and 'Intellivue/PEEP_CMH2O' in tracks:
        possible_list.append('Driving Pressure')
    if 'Intellivue/Tidal_Volume' in tracks and 'Driving Pressure' in possible_list:
        possible_list.append('Compliance')
    if 'Intellivue/PLETH_SAT_O2' and 'Intellivue/FiO2' in tracks:
        possible_list.append('ROX Index')
    if ('Intellivue/BT_CORE' or 'Intellivue/BT_BLD') and ('Intellivue/BT_SKIN' or 'Intellivue/TEMP') in tracks:
        possible_list.append('Temp Comparison')
    #Pendiente Comprobar Variables MostCare
    #Pendiente Comprobar Variables autonomicas

    if 'Intellivue/ICP' in tracks: #Might need more variables
        possible_list.append('ICP Model')
    #Pendiente comprobar ABP model
    #Pendiente Comprobar otros algoritmos

    return possible_list #Esta lista se envía al front para que el usuario seleccione.

#Falta una función que reciba el selected_list desde el front. 

def run_selected(selected_list): #Función que ejecuta los algoritmos seleccionados.
    results = {}
    for algorithm in selected_list:
        if algorithm == 'Shock Index':
            results['Shock Index'] = ShockIndex(vf).values
        elif algorithm == 'Driving Pressure':
            results['Driving Pressure'] = DrivingPressure(vf).values
        elif algorithm == 'Compliance':
            results['Compliance'] = Compliance(vf).values
        elif algorithm == 'ROX Index':
            results['ROX Index'] = RoxIndex(vf).values
        elif algorithm == 'Temp Comparison':
            results['Temp Comparison'] = TempComparison(vf).values 
            #Gestionar distinto, devuelve un array con dos señales.
        
        #Pendiente añadir variables MostCare
        #Pendiente añadir Variables autonomicas
        elif algorithm == 'ICP Model':
            results['ICP Model'] = icp_model() #Pendiente ver como añadir el modelo de ICP
        
        #Pendiente añadir ABP model
        #Pendiente añadir otros algoritmos.
    return results

#ROX INDEX
def rox_index():
    return vf.to_numpy(track_names = 'Intellivue/PLETH_SAT_O2') / vf.to_numpy(track_names = 'Intellivue/FiO2')

