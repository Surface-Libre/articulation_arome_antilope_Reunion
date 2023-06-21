set "VORTEX_HOME=C:\Users\33751\Vortex\build\distributions\vortex-0.11.0-dev.0+616f150"
set "PATH=%VORTEX_HOME%\bin;%VORTEX_HOME%\bin\gdal;%PATH%"
set "GDAL_DATA=%VORTEX_HOME%\bin\gdal\gdal-data"
set "PROJ_LIB=%VORTEX_HOME%\bin\gdal\projlib"
set "CLASSPATH=%VORTEX_HOME%\lib\*"


C:\Users\33751\Downloads\jython2.7.3\bin\jython.exe -J-Xmx2g -Djava.library.path=%VORTEX_HOME%\bin;%VORTEX_HOME%\bin\gdal C:\Users\33751\Desktop\artic_arome_antilope\batches\import_AROME.py

