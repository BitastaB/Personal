import bpy
import sys
import os
from mathutils import *   


############ To import other .py files ####################################

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
import dataset
#import table

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib

importlib.reload(dataset)
from dataset import *
#importlib.reload(table)
#from table import *
#for module in sys.modules.values():
#    importlib.reload(module)
#    print("** printing module reloaded **",module)
    #from module import *

##########################################################################    
    
    
print("\n... Starting generate.py ...")
for obj in bpy.context.scene.objects:
     if obj.type == 'MESH':    
         bpy.data.objects.remove(obj, do_unlink=True)
         
ladder = generate_ladder(-3, 0, 2)
table = generate_table(1, 0, 2)
laptop = generate_laptop(6,0,2)
pinnochio = generate_pinnochio_male(-1, 0, 2)
pinnochio_female = generate_pinnochio_female(3, 0, 2)
print("... Exiting generate.py ...")
