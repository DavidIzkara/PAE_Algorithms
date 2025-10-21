import vitaldb
from shock_index import ShockIndex
from driving_pressure import DrivingPressure
from compliance import Compliance
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
    if 'Intellivue/TEMP' and 'Intellivue/BT_CORE' and 'Intellivue/BT_SKIN' in tracks:
        possible_list.append('Temp Comparison') #Pendiente actualizar esta función.

    #Pendiente Comprobar lo necesario para el modelo de ICP
    #Pendiente Comprobar Variables autonomicas
    #Pendiente Comprobar MustCare

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
            results['ROX Index'] = rox_index()
        #elif algorithm == 'Temp Comparison':
        #    results['Temp Comparison'] = temp_comparison()
        #Pendiente añadir los algoritmos que hayan sido previamente comprobados.
    return results

#ROX INDEX
def rox_index():
    return vf.to_numpy(track_names = 'Intellivue/PLETH_SAT_O2') / vf.to_numpy(track_names = 'Intellivue/FiO2')

