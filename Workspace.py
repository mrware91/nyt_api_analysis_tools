import os
import pickle
CodeDir="/home/mrware/Dropbox/Code/NYTimes API"

WorkspaceObjects=[]

def save_obj(obj, name ):
    folder=CodeDir+'/obj/'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(folder + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    folder=CodeDir+'/obj/'
    try:
        with open(folder + name + '.pkl', 'rb') as f:
            print name+" remembered!"
            return pickle.load(f)
    except IOError:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        save_obj({},name)
        return {}

def det_fn_name(fn ):
    idx1=str(fn).index('at')
    idx0=str(fn).index(' ')
    return str.strip(str(fn)[idx0:idx1])

def save_workspace():
    for obj in WorkspaceObjects:
        print "Saving %s ..." % obj
        globals()[obj].make_memory()
    print "Done!"

def clear_workspace():
    for obj in WorkspaceObjects:
        print "Clearing %s ..." % obj
        globals()[obj].forget()
    print "Done!"

def clean_slate():
    for obj in WorkspaceObjects:
        print "Clearing %s ..." % obj
        globals()[obj].forget()
    print "Done!"
