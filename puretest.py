#make an absolute path a relative path base on an absolute path.

import os

abs_path = os.path.abspath('./save/sm(C)')

#change a latex file_dict to new file_dict with relative files
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
