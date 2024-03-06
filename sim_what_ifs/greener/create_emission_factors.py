import yaml
import pandas as pd
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)
import regions

yamlfiledir = '../../shared_data/emission_factors_yaml'
default_emission_file = f"{yamlfiledir}/defaults.yaml"
filename = 'data_output/emission_factors.csv'

emission_source = [
                     'biomass', 
                     'coal', 
                     'gas', 
                     'geothermal',
                     'hydro',  
                     'nuclear',
                     'oil', 
                     'solar',
                     'wind', 
                     'unknown'
                    ]

zone_code_list = regions.get_year_order()

with open(default_emission_file, "r") as default_file: 
    default_obj = yaml.safe_load(default_file)["emissionFactors"]["lifecycle"]

dfcolumns = ["zone_code"]
dfcolumns.extend(emission_source)
emission_factor_df = pd.DataFrame(columns=dfcolumns)
for zonecode in zone_code_list: 
    

    yamlfile = f"{yamlfiledir}/{zonecode}.yaml"
    

    with open(yamlfile,"r") as file: 
        yaml_obj = yaml.safe_load(file)


    zone_emission_factors = yaml_obj["emissionFactors"]["lifecycle"].keys()

    newrow = []
    newrow.append(zonecode)
    for e_factor in emission_source: 
        if e_factor not in zone_emission_factors: 
            emission_factor = default_obj[e_factor]['value']
            pass
        else: 
            factor = yaml_obj["emissionFactors"]["lifecycle"][e_factor]
            objtype = type(factor)
            
            isList = (factor.__class__ == list)
            if isList: 
                emission_factor = yaml_obj["emissionFactors"]["lifecycle"][e_factor][0]['value']
            else:
                emission_factor = yaml_obj["emissionFactors"]["lifecycle"][e_factor]['value']
        
        newrow.append(emission_factor)
    emission_factor_df.loc[len(emission_factor_df.index)] = newrow



emission_factor_df.to_csv(filename,index=False)
