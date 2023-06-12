from mil.army.usace.hec.vortex.io import BatchImporter
from mil.army.usace.hec.vortex.geo import WktFactory

from glob import glob

in_files = glob(r'C:/Users/33751/Desktop/artic_arome_antilope/results/asc/antilope/*.asc')

variables = ['*']

geo_options = {
   }

destination = 'C:/Users/33751/Desktop/artic_arome_antilope/results/dss/dss_central.dss'

write_options = {
    'partA': 'A',
    'partB': 'A',
    'partC': '',
    'partF': 'A',
    'dataType': 'PER-CUM',
    'units': 'MM'
}

myImport = BatchImporter.builder() \
    .inFiles(in_files) \
    .variables(variables) \
    .geoOptions(geo_options) \
    .destination(destination) \
    .writeOptions(write_options) \
    .build()

myImport.process()