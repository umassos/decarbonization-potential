import os 

def check_dir(path): 
    if not os.path.exists(path): 
        os.mkdir(path)