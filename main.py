"""
This script imports data from AROME and Antilope sources into a DSS central system.
"""

import time
import os
from multiprocessing import Process

from arome_antilope_importation import DataImporter


# Define file and folder paths
folder_arome_nc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\data\\AROME\\'
folder_arome_asc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\arome\\brut\\'
folder_arome_asc_artic = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\arome\\articulation_quart\\'
batch_file_path_arome_quart = r"C:\Users\33751\Desktop\artic_arome_antilope\batches\import_AROME.bat"

antilope_filepath_nc = 'C:\\Users\\33751\Desktop\\artic_arome_antilope\\data\\antilope_tr_000015.nc'
folder_antilope_asc = 'C:\\Users\\33751\\Desktop\\artic_arome_antilope\\results\\asc\\antilope\\'
batch_file_path_antilope =r"C:\Users\33751\Desktop\artic_arome_antilope\batches\import_ANTILOPE.bat"

# Initialize variables for tracking time intervals
antilope_import_sleep = 20  # 20 seconds
arome_import_sleep = 30  # 30 seconds


def antilope_import():
    """
    Continuously monitors the Antilope file and imports data into DSS central when modified.
    """
    while True:
        try:
            initial_modified_date = os.path.getmtime(antilope_filepath_nc)

            while True:
                modified_date = os.path.getmtime(antilope_filepath_nc)
                if modified_date != initial_modified_date:
                    # Perform DSS operations
                    DataImporter.antilope_importation(antilope_filepath_nc, folder_antilope_asc,
                                                      batch_file_path_antilope)

                    initial_modified_date = modified_date
                else:
                    print("Antilope file is not modified yet")

                time.sleep(antilope_import_sleep)

        except Exception as e:
            # Handle any exceptions that may occur during execution
            print("An error occurred in Antilope Importation to DSS central:", str(e))

        # Delay for the specified interval
        time.sleep(antilope_import_sleep)


def arome_import():
    """
    Continuously monitors the AROME folder and imports data into DSS central when modified.
    """
    while True:
        try:
            initial_modified_date = os.path.getmtime(folder_arome_nc)

            while True:
                modified_date = os.path.getmtime(folder_arome_nc)
                if modified_date != initial_modified_date:
                    # Perform DSS operations
                    DataImporter.arome_importation_quart(folder_arome_nc, folder_arome_asc,
                                        folder_arome_asc_artic, batch_file_path_arome_quart)

                    initial_modified_date = modified_date
                else:
                    print("Arome is not modified yet")

                time.sleep(arome_import_sleep)

        except Exception as e:
            # Handle any exceptions that may occur during execution
            print("An error occurred in AROME Importation to DSS central", str(e))

        # Delay for the specified interval
        time.sleep(arome_import_sleep)


if __name__ == '__main__':
    # Create and start separate processes for CSV monitoring and DSS operations
    arome_import_process = Process(target=arome_import)
    antilope_import_process = Process(target=antilope_import)

    arome_import_process.start()
    antilope_import_process.start()

    # Wait for the processes to complete
    arome_import_process.join()
    antilope_import_process.join()
