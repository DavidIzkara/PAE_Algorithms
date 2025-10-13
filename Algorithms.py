import vitaldb
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
        possible_list.append('Temp Comparison')

    return possible_list #Esta lista se envía al front para que el usuario seleccione.

#Falta una función que reciba el selected_list desde el front. 

def run_selected(selected_list): #Función que ejecuta los algoritmos seleccionados.
    results = {}
    for algorithm in selected_list:
        if algorithm == 'Shock Index':
            results['Shock Index'] = shock_index()
        elif algorithm == 'Driving Pressure':
            results['Driving Pressure'] = driving_pressure()
        elif algorithm == 'Compliance':
            results['Compliance'] = compliance()
        elif algorithm == 'ROX Index':
            results['ROX Index'] = rox_index()
        #elif algorithm == 'Temp Comparison':
        #    results['Temp Comparison'] = temp_comparison()
    return results

#SHOCK INDEX (if there is invasive blood pressure, use it; if not, use non-invasive blood pressure)
def shock_index():
    try:
        SI = vf.to_numpy(track_names = 'Intellivue/ECG_HR') / vf.to_numpy(track_names = 'Intellivue/ABP_SYS')  # Invasive blood pressure
    except Exception:
        SI = vf.to_numpy(track_names = 'Intellivue/ECG_HR') / vf.to_numpy(track_names = 'Intellivue/NIBP_SYS')  # Non-invasive blood pressure
    return SI

#DRIVING PRESSURE
def driving_pressure():
    return vf.to_numpy(track_names = 'Intellivue/PPLAT_CMH2O') - vf.to_numpy(track_names = 'Intellivue/PEEP_CMH2O')

#COMPLIANCE
def compliance():
    return vf.to_numpy(track_names = 'Intellivue/Tidal_Volume') / driving_pressure() 

#ROX INDEX
def rox_index():
    return vf.to_numpy(track_names = 'Intellivue/PLETH_SAT_O2') / vf.to_numpy(track_names = 'Intellivue/FiO2')

