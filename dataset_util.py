import bpy
from mathutils import *
import numpy as np  


#### Set child object to a parent object with transform
def set_child_to_parent(child, parent):
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()