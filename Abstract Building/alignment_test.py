def delete_math_data(self,simplex,**kwargs):
    type = simplex.math_data.type

    if math_data.type == 'golog':
        golog_dict = simplex.math_data()
        #remove close window and remove mode_head if it has
        golog = golog_dict['golog']
        #if it's list of mode_heads is not empty
        if hasattr(golog,'mode_heads'):
            for mode_head in golog.mode_heads:
                if mode_head.has_window:
                    if hasattr(mode_head,'windict'):
                        if 'win' in mode_head.windict.keys():
                            self.base.closeWindow(mode_head.windict['win'], keepCamera = True, removeWindow = True)
                mode_head.reset()
                mode_head.clean()

        folder_path = os.path.join(self.folder_path, *golog_dict['folder_path'])
        tk_funcs.ask_delete_path(folder_path)

    elif math_data.type == 'file':
        abs_file_path = os.path.join(self.folder_path,*simplex.math_data())
        tk_funcs.ask_delete_path(abs_file_path)

    elif math_data.type == 'latex':
        folder = os.path.join(self.folder_path, simplex.math_data()['folder'])
        tk_funcs.ask_delete_path(folder)

    simplex.math_data = hcat.Math_Data(type = 'None')

def delete_graphics_data(self,graphics,**kwargs):
    graphics.node
