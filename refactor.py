import pandas as pd
import os
import re

def get_data(file_path:str,i):
    file = pd.read_csv(file_path,usecols=[i],engine='python')
    file_values = file.values
    return file_values

def refactor_one(path):
    """
    直接相加为最终数据
    """
    values = 0

    FileNames = os.listdir(path)
    # print("FileNames:\n",FileNames)
    for fn in FileNames:
        if fn.startswith('IMF'):
            # print("fn:\n",fn)
            fullfilename = os.path.join(path, fn)
            values += get_data(fullfilename,0)
    return values

def save_data(K,values):
    dataframe = pd.DataFrame(values / K)
    dataframe.columns=["refactor_data"]
    dataframe.to_csv(r"./vmd/refactor.csv",index=False,sep=',')  

def run():
    K =5
    path = r"./vmd/" 
    values = refactor_one(path)

    save_data(K,values)
    




if __name__ == "__main__":
    
    run()