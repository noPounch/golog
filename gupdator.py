# A file for updating gologs from one version to the next
# takes in a gimported golog, reads its version, updates to next version
# todo: put a version number in gexport, put a version number at header of run
# create a file of archived gimports
import os, pickle
from hcat import Simplex, Math_Data
import golog_export


def update_latex(root_name,file_dict):


    def get_rel_path(root_name, abs_path):

        def strip_path_to_save(abs_path,rel_path):
            if os.path.split(abs_path)[1] == root_name:
                return os.path.join(*rel_path)
            else:
                a = strip_path_to_save(os.path.split(abs_path)[0], [os.path.split(abs_path)[1]] + rel_path)
                print('irea',a)
                return a
        return strip_path_to_save(abs_path,[])

    relative_folder = get_rel_path(root_name,file_dict['folder'])
    new_file_dict  = {'folder':relative_folder,'tex':os.path.join(relative_folder,file_dict['name']+'.tex')}

    return new_file_dict

def gupdateNONEtoV1_0_0(export_sSet):
    export_version = '1.0.0'
    #added in updates to 1.0.0:
    # added versioning to exports
    # made latex pathing independent of platform

    # update latex type to prevent pathing issues
    for simp in export_sSet.rawSimps:
        #check if export_math_data is of filetype 'latex'
        if simp.math_data().exported_math_data.type == 'latex':
            new_file_dict = update_latex('sm(C)',simp.math_data().exported_math_data())
            simp.math_data().exported_math_data = Math_Data(type = 'latex', math_data = new_file_dict)


        #      #^export_data #^orig math_data


    export_simplex = Simplex(0,math_data = Math_Data(type = 'exported golog',math_data = export_sSet)) #create a simplex from the export_sSet
    export_meta = golog_export.export_data(export_simplex, export_version = export_version) # create meta_data in the form of export_data

    return export_meta

def gupdate(export_object):
    #will eventually be a list of update procedures
    pass

#
file_path = os.path.abspath('./save/sm(C)/sm.golog')
# print(os.path.exists(file_path),file_path)
with open(file_path, 'rb') as file:
    export_sSet = pickle.load(file)
e = gupdateNONEtoV1_0_0(export_sSet)


new_file_path = file_path.split('.')[0]+'(1_0_0).golog'
with open(new_file_path, 'wb') as file:
     pickle.dump(e,file)
