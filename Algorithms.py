import vitaldb 
from vitaldb import VitalFile

from Algoritmos_VF.shock_index import ShockIndex
from Algoritmos_VF.driving_pressure import DrivingPressure
from Algoritmos_VF.dynamic_compliance import DynamicCompliance
from Algoritmos_VF.rox_index import RoxIndex
from Algoritmos_VF.temp_comparison import TempComparison
from Algoritmos_VF.cardiac_output import CardiacOutput
from Algoritmos_VF.systemic_vascular_resistance import SystemicVascularResistance
from Algoritmos_VF.cardiac_power_output import CardiacPowerOutput
from Algoritmos_VF.effective_arterial_elastance import EffectiveArterialElastance

#Pendiente importar ICP Model
#Pendiente importar ABP Model

#Pendiente importar otros algoritmos


#Este código va en back-end, las definiciones de las variables ya están hechas, es solo para ver cómo se usa la clase.:

vital_path = find_latest_vital(recordings_dir) #Función que encuentra el último fichero de vital.
vf = VitalFile(vital_path) # Aquí esta todo el fichero.
tracks = vf.get_track_names() #Aquí están todos los nombres de las variables.
raw = vf.to_numpy(tracks, interval=0, return_timestamp=True) #Aquí están todos los datos en bruto.

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

#Falta una función que reciba el selected_list desde el front. 

def run_selected(selected_list): #Función que ejecuta los algoritmos seleccionados.
    results = {}
    for algorithm in selected_list:
        if algorithm == 'Shock Index':
            results['Shock Index'] = ShockIndex(vf).values
        elif algorithm == 'Driving Pressure':
            results['Driving Pressure'] = DrivingPressure(vf).values
        elif algorithm == 'Dynamic Compliance':
            results['Dynamic Compliance'] = DynamicCompliance(vf).values
        elif algorithm == 'ROX Index':
            results['ROX Index'] = RoxIndex(vf).values
        elif algorithm == 'Temp Comparison':
            results['Temp Comparison'] = TempComparison(vf).values
              #Gestionar distinto, devuelve un array con dos señales.
        elif algorithm == 'Cardiac Output':
            results['Cardiac Output'] = CardiacOutput(vf).values
        elif algorithm == 'Systemic Vascular Resistance':
            results['Systemic Vascular Resistance'] = SystemicVascularResistance(vf).values
        elif algorithm == 'Cardiac Power Output':
            results['Cardiac Power Output'] = CardiacPowerOutput(vf).values
        elif algorithm == 'Effective Arterial Elastance':
            results['Effective Arterial Elastance'] = EffectiveArterialElastance(vf).values
        
        #Pendiente añadir Variables autonomicas
        elif algorithm == 'ICP Model':
            results['ICP Model'] = icp_model() #Pendiente ver como añadir el modelo de ICP
        elif algorithm == 'ABP Model':
            results['ABP Model'] = abp_model() #Pendiente ver como añadir el modelo de ABP

        #Pendiente añadir otros algoritmos.
    return results


