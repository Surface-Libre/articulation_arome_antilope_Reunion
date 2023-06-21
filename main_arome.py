"""
This script imports data from AROME sources into a DSS central system.
"""

import os
import time
from arome_antilope_importation import DataImporter


# Define file and folder paths
folder_arome_nc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\data\\AROME\\'
folder_arome_asc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\arome\\brut\\'
folder_arome_asc_artic = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\arome\\articulation_quart\\'
dss_central_filepath='C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\dss\\dss_central.dss'
arome_runs_folder='C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\runs_dss_arome\\'
batch_file_path_arome_quart = r"C:\Users\33751\Desktop\artic_arome_antilope\batches\import_AROME.bat"


def arome_import():
    """
    Continuously monitors the AROME folder and imports data into DSS central when modified.
    """
    
    try:
        # Perform DSS operations
        DataImporter.arome_importation_quart(folder_arome_nc, folder_arome_asc, folder_arome_asc_artic,
                                            batch_file_path_arome_quart,dss_central_filepath, 
                                            arome_runs_folder)
    except Exception as e:
        # Handle any exceptions that may occur during execution
        print("An error occurred in Antilope Importation to DSS central:", str(e))
            # Perform DSS operations
            
        

if __name__ == '__main__':
    arome_import()