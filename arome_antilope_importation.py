import os
import shutil
import subprocess
import datetime
import netCDF4 as nc
from osgeo_utils import gdal_calc


class DataImporter:
    """
    A class for importing and processing data using multiprocessing.

    Attributes:
        None
    """

    @staticmethod
    def write_prj_wkt(prj_file_path):
        """
        Write PROJCS well-known text (WKT) to a projection file.

        Args:
            prj_file_path (str): Path to the projection file.

        """
        with open(prj_file_path, 'w') as prj_file:
            prj_file.write('PROJCS["RGR_1992_UTM_40S",GEOGCS["GCS_RGR_1992",DATUM["D_RGR_1992",'
                           'SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],'
                           'UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],'
                           'PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],'
                           'PARAMETER["Central_Meridian",57.0],PARAMETER["Scale_Factor",0.9996],'
                           'PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')

    @staticmethod
    def extract_quarter_hour_arome(filename_datetime_asc):
        """
        Extract quarter-hour intervals from a given filename.

        Args:
            filename_datetime_asc (str): Filename in the format of 'YYYY_MM_ddtHHMM_HHMM'.

        Returns:
            list: List of quarter-hour interval strings.
        """
        # Split the datetime string into start and end datetime strings
        start_str, end_str = filename_datetime_asc[0:15], filename_datetime_asc[16:]

        # Convert the start and end datetime strings into datetime objects
        start_datetime = datetime.datetime.strptime(start_str, '%Y_%m_%dt%H%M')
        end_datetime = datetime.datetime.strptime(end_str, '%Y_%m_%dt%H%M')

        # Define the 15-minute interval timedelta
        interval = datetime.timedelta(minutes=15)

        # Iterate over the intervals and store them in a list
        current_datetime = start_datetime
        intervals = []

        while current_datetime < end_datetime:
            interval_end = current_datetime + interval
            interval_str = f"{current_datetime.strftime('%Y_%m_%dt%H%M')}_{interval_end.strftime('%Y_%m_%dt%H%M')}"
            intervals.append(interval_str)
            current_datetime += interval

        return intervals

    @staticmethod
    def remove_files(folder_path):
        """
        Remove all files within a folder.

        Args:
            folder_path (str): Path to the folder.

        Returns:
            None
        """
        # Get the list of files in the folder
        files = os.listdir(folder_path)

        # Iterate over the files and delete them
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    @staticmethod
    def last_run_arome_dss(source_path, destination_path):
        """
        Copy a DSS file AROME with last Antilope Changes from source path to destination path.

        Args:
            source_path (str): Path to the source file.
            destination_path (str): Path to the destination file.

        Returns:
            None
        """
        shutil.copy(source_path, destination_path)

    @staticmethod
    def arome_importation_quart(folder_arome_nc, folder_arome_asc, folder_arome_asc_artic, batch_file_path_arome_quart, dss_central_filepath, arome_runs_folder):
        """
        Import and process Arome data in quarter-hour intervals.

        Args:
            folder_arome_nc (str): Path to the folder containing Arome NetCDF files.
            folder_arome_asc (str): Path to the folder where Arome ASCII files will be saved.
            folder_arome_asc_artic (str): Path to the folder where processed Arome ASCII files will be saved.
            batch_file_path_arome_quart (str): Path to the batch file for Arome quarter-hour processing.

        Returns:
            None
        """
        time_historique_arome = []

        DataImporter.remove_files(folder_arome_asc_artic)
        DataImporter.remove_files(folder_arome_asc)

        for filename_nc in os.listdir(folder_arome_nc):
            if filename_nc.endswith('.nc'):
                nc_path = os.path.normpath(os.path.join(folder_arome_nc, filename_nc))
                nc_file = nc.Dataset(nc_path, 'r')

                # Get the variable you want to convert to ASCII
                times = nc_file.variables['time'][:][0]

                date_value = datetime.datetime.strptime(str(int(times)), '%Y%m%d')
                time_value = datetime.timedelta(seconds=round((times % 1) * 86400))
                result = date_value + time_value
                filename_datetime_asc = result.strftime('%Y_%m_%dt%H%M') + '_' + (
                            result + datetime.timedelta(hours=1)).strftime('%Y_%m_%dt%H%M')
                time_historique_arome.append(result.strftime('%Y-%m-%d %H:%M'))
                filepath_asc = os.path.normpath(os.path.join(folder_arome_asc, f"{filename_datetime_asc}.asc"))
                subprocess.call(['gdal_translate', '-of', 'AAIGrid', nc_path, filepath_asc])
                prj_file_path_arome = os.path.join(folder_arome_asc, f"{filename_datetime_asc}.prj")
                DataImporter.write_prj_wkt(prj_file_path_arome)

                for filename_quart_asc in DataImporter.extract_quarter_hour_arome(filename_datetime_asc):
                    print(filename_quart_asc)
                    filepath_asc_quar_asc = os.path.normpath(os.path.join(folder_arome_asc_artic, f"{filename_quart_asc}.asc"))
                    print(filepath_asc_quar_asc)
                    tif_quar = gdal_calc.Calc(calc="A/4", A=filepath_asc, format="GTiff",
                                              outfile=filepath_asc_quar_asc)
                    prj_file_path_arome = os.path.join(folder_arome_asc_artic, f"{filename_quart_asc}.prj")
                    DataImporter.write_prj_wkt(prj_file_path_arome)

                nc_file.close()
        
        # Copy the file with a new name to another folder
        run_arome_filename = f"AROME_Run_{datetime.datetime.strptime(time_historique_arome[0], '%Y-%m-%d %H:%M').strftime('%Y_%m_%dt%H%M')}_{datetime.datetime.strptime(time_historique_arome[-1], '%Y-%m-%d %H:%M').strftime('%Y_%m_%dt%H%M')}.dss"
        run_arome_filepath= os.path.normpath(os.path.join(arome_runs_folder, run_arome_filename))
        DataImporter.last_run_arome_dss(dss_central_filepath, run_arome_filepath)

        subprocess.run([batch_file_path_arome_quart])
        
        print(f'Importation Arome entre {time_historique_arome[0]} et {time_historique_arome[-1]} est terminée')

    @staticmethod
    def antilope_importation(antilope_filepath_nc, folder_antilope_asc, batch_file_path_antilope):
        """
        Import and process Antilope data.

        Args:
            antilope_filepath_nc (str): Path to the Antilope NetCDF file.
            folder_antilope_asc (str): Path to the folder where Antilope ASCII files will be saved.
            batch_file_path_antilope (str): Path to the batch file for Antilope processing.

        Returns:
            None
        """
        time_historique_antilope = []

        DataImporter.remove_files(folder_antilope_asc)

        nc_file = nc.Dataset(antilope_filepath_nc, 'r')

        # Get the variable you want to convert to ASCII
        times = nc_file.variables['time'][:][0]

        date_value = datetime.datetime.strptime(str(int(times)), '%Y%m%d')
        time_value = datetime.timedelta(seconds=round((times % 1) * 86400))
        result = date_value + time_value
        filename_datetime_asc = result.strftime('%Y_%m_%dt%H%M') + '_' + (
                result + datetime.timedelta(minutes=15)).strftime('%Y_%m_%dt%H%M')
        time_historique_antilope.append(result.strftime('%Y-%m-%d %H:%M'))
        filepath_asc = os.path.normpath(os.path.join(folder_antilope_asc, f"{filename_datetime_asc}.asc"))
        subprocess.call(['gdal_translate', '-of', 'AAIGrid', antilope_filepath_nc, filepath_asc])
        prj_file_path_arome = os.path.join(folder_antilope_asc, f"{filename_datetime_asc}.prj")
        DataImporter.write_prj_wkt(prj_file_path_arome)
        nc_file.close()

        subprocess.run([batch_file_path_antilope])


        print(f'Importation Antilope entre {time_historique_antilope[0]} et {time_historique_antilope[-1]} '
              f'est terminée')
