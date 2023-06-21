"""
This script imports data from Antilope sources into a DSS central system.
"""

import time
import os

from arome_antilope_importation import DataImporter


# Define file and folder paths
antilope_filepath_nc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\data\\antilope_tr_000015.nc'
folder_antilope_asc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\antilope\\'
batch_file_path_antilope = r"C:\Users\33751\Desktop\artic_arome_antilope\batches\import_ANTILOPE.bat"


def antilope_import():
    """
    Continuously monitors the Antilope file and imports data into DSS central when modified.
    """
    
    try:
        # Perform DSS operations
        DataImporter.antilope_importation(antilope_filepath_nc, folder_antilope_asc, batch_file_path_antilope)
    except Exception as e:
        # Handle any exceptions that may occur during execution
        print("An error occurred in Antilope Importation to DSS central:", str(e))

if __name__ == '__main__':
    antilope_import()
