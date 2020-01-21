#takes a golog, simplicial set => JSON Universe 

#Set a starting sset for the golog
#For each simplex in golog, give it a unique ID

#For each math_data type in golog, give it a unique ID
#Handle each type of data
#Save External files in on big folder, referenced by the ID


#Takes a JSON Universe => A golog, who's starting point is given in the meta_data
import os, sys
sys.path.append(os.path.abspath('.'))
# import ../db.py
import hcat, random, golog
from panda3d.core import LPoint3f

def GSON(Golog):
    #put everything into a JSON file without any structure, just references
    GSON = dict()
    pyobject_to_id = dict()

    #starting golog
    # pyobject_to_id[golog] = '00000000'

    def generate_id(pyobject):
        string = '00000000' #starting string
        while string in pyobject_to_id.values(): string = ''.join([str(random.randrange(10)) for i in range(8)])
        return string
    
    def serialize(pyobject):
       

        if pyobject in pyobject_to_id.keys(): return pyobject_to_id[pyobject]
        id = generate_id(pyobject)
        pyobject_to_id[pyobject] = id
        
        if isinstance(pyobject, hcat.Simplex):

            ob_dict = {
                'type' : 'Simplex',
                'meta' : {'label':pyobject.label, 'id': pyobject_to_id[pyobject],'level':pyobject.level},
                'faces': [serialize(face) for face in pyobject.faces]
            }
            
            ob_dict['math_data_type'] = math_data_type = pyobject.math_data.type
            if math_data_type == 'golog': ob_dict['math_data'] = {'golog':serialize(pyobject.math_data()['golog']),'folder_path':pyobject.math_data()['folder_path']}
            elif math_data_type in ['file','latex','None','weblink','link','simpSet'] : ob_dict['math_data'] = pyobject.math_data()
            else: print(math_data_type +' unhandled by gexport')
        

        elif isinstance(pyobject, golog.golog):
            pos_dict = dict()
            for simplex in pyobject.sSet.rawSimps: 
                pos_dict[serialize(simplex)] = list(pyobject.Simplex_to_Graphics[simplex].graphics_kwargs['pos'])


            ob_dict= {
                'type': 'golog',
                'meta': {'label':pyobject.label, 'id': pyobject_to_id[pyobject]},
                'pos_dict' : pos_dict
            }
        
        if pyobject_to_id[pyobject] not in GSON.keys(): GSON[pyobject_to_id[pyobject]] = ob_dict
        return pyobject_to_id[pyobject]
            
    serialize(Golog)
    return GSON

def load_GSON(base, GSON, **kwargs):
    #create golog from GSON
    handled = dict()

    #create a golog from dict entry in GSON
    def load_golog_dict(golog_index):
        print(type(golog_index))
        if golog_index in handled.keys() : return handled[golog_index]
        G = golog.golog(base, label = GSON[golog_index]['meta']['label'], **kwargs)
        handled[GSON[golog_index]['meta']['id']] = G
        for simp_key in GSON[golog_index]['pos_dict'].keys():
            load_simplex_dict(simp_key, golog_index)
        
        return G

    def load_simplex_dict(simp_index, golog_index):
        simp_dict = GSON[simp_index]
        if simp_index in handled : return handled[simp_index]
        faces = tuple([load_simplex_dict(face_key, golog_index) for face_key in simp_dict['faces']])

        
        #handle math_data, if golog, change into an anctual golog
        if simp_dict['math_data_type'] == 'golog':
            golog_dict = {
                'golog':load_golog_dict(simp_dict['math_data']['golog']),
                'folder_path':simp_dict['math_data']['folder_path']
                }
            math_data = hcat.Math_Data(type = 'golog', math_data = golog_dict)
        else: math_data = hcat.Math_Data(type = simp_dict['math_data_type'],math_data =  simp_dict['math_data'])

        G = load_golog_dict(golog_index)
        simp = G.add(
            faces, 
            label = simp_dict['meta']['label'], 
            math_data = math_data,
            pos = LPoint3f(*GSON[golog_index]['pos_dict'][simp_index])
        )


        return simp
    
    return load_golog_dict('00000000')


    


def load_GSON_file(base, path):
    pass


if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase
    from golog_export import gimport
    from window_manager import modeHeadToWindow
    from mode_head import mode_head
    base = ShowBase(windowType = 'none')
    G = gimport(base,
        os.path.abspath('./user_files/save/Adjoint School Ontology/Adjoint School Ontology.golog'),
        model_path = os.path.abspath('./misc_data/models/')
    )
    with open(os.path.join( os.path.dirname( os.path.abspath(__file__) ) , 'test/test.json' )) as json 

    GSON = GSON(G)
    golog = load_GSON(base, GSON)
    # controllable_golog = mode_head(base,golog, folder_path = os.path.abspath('./user_files/save/test'))
    # modeHeadToWindow(base, controllable_golog)