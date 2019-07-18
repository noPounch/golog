# A file for updating gologs from one version to the next
# takes in a gimported golog, reads its version, updates to next version
# todo: put a version number in gexport, put a version number at header of run
# create a file of archived gimports
import os, pickle
from hcat import Simplex, Math_Data
import golog_export

export_version = '1.0.0'

def gupdateNONEtoV1_0_0(export_sSet):
    #added in updates to 1.0.0:
    # added versioning to exports
    # made latex pathing independent of platform

    # update latex type to prevent pathing issues
    for simp in export_sSet.rawSimps:
        #check if export_math_data is of filetype 'latex'
        if simp.math_data().exported_math_data.type == 'latex':
            simp.math_data().exported_math_data()['folder'] = os.path.abspath(simp.math_data().exported_math_data()['folder'])
        #      #^export_data #^orig math_data


    export_simplex = Simplex(0,math_data = Math_Data(type = 'exported golog',math_data = export_sSet)) #create a simplex from the export_sSet
    export_meta = golog_export.export_data(export_simplex, export_version = export_version) # create meta_data in the form of export_data

    return export_meta


file_path = os.path.abspath('./save/sm(C)/sm.golog')
print(os.path.exists(file_path),file_path)
with open(file_path, 'rb') as file:
    export_sSet = pickle.load(file)
e = gupdateNONEtoV1_0_0(export_sSet)
new_file_path = file_path.split('.')[0]+'(1_0_0).golog'
with open(new_file_path, 'wb') as file:
     pickle.dump(e,file)
