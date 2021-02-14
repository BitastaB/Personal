import bpy
from bpy.app.handlers import persistent

print("Starting...")

frame_read_counter = []
scene_objects_dict = {}
energy_unit = 1

class SceneObject:
  
  def __init__(self, name):
      print(f"Initialising {name}")
      self.name = name 
      self._location = []
      self._moving = False
      self._volume = 0
      print("initalisation complete")
    
 # @property
  def get_location(self,i):
      """I'm the location of the scene object."""
      return self._location[i]

 # @loc.setter
  def set_location(self, loc):
      self._location.append(loc) 
      
      
  def get_by_name(self, name):
      if(self.name == name):
          return self    

  def set_moving(self, isMoving):
       self._moving = isMoving
       

  def set_volume(self, vol):
     self._volume = vol     
    


############ Calculate volume of objects
# Quick way to test with/without hidden faces
USE_FILTER_FACES = True

def is_face_skip(f):
    """Ignore faces that pass this test!"""
    return f.hide is False
    # If want to filter based on material.
    # return f.material_index == 0
    
    
def bmesh_from_object_final(ob):
    import bmesh
    matrix = ob.matrix_world
    me = ob.to_mesh()
    me.transform(matrix)
    bm = bmesh.new()
    bm.from_mesh(me)
    if USE_FILTER_FACES:
        faces_remove = [f for f in bm.faces if not is_face_skip(f)]
        for f in faces_remove:
            bm.faces.remove(f)
    return (bm, matrix.is_negative)


def volume_from_object(ob):
    bm, is_negative = bmesh_from_object_final(ob)
    volume = bm.calc_volume(signed=True)
    #area = sum(f.calc_area() for f in bm.faces)
    bm.free()
    if is_negative:
        volume = -volume
    return volume#, area

############ Set global scene properties 
def set_scene_properties():
    
    i=100
    print("\nSetting scene properties")
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH':
        so = SceneObject(obj.name)
        vol = volume_from_object(obj)
        so.set_volume(vol) 
        scene_objects_dict[obj.name] = so
              
        
    print("Total objects in current scene : " + str(len(scene_objects_dict)))

                  
########### Process location/rotation of objects during animation                
def process_obj_location(scene):    
    if scene.frame_current in frame_read_counter:
        return
    print(f"\nProcessing all object locations for frame : {str(scene.frame_current)}") 
    for obj in bpy.context.scene.objects:
    #for obj in scene.objects:
      if obj.type == 'MESH': 
          location = obj.matrix_world@obj.location
          object_instance = scene_objects_dict.get(obj.name, None)
          object_instance.set_location(location)
    
    frame_read_counter.append(scene.frame_current)
    print(f"Finished processing locations for frame {str(scene.frame_current)}")


 
########## Analyse object movement post animation   
def analyse_scene():
    print("\nAnimation over, will analyse scene now")
    
    move_change_counter = {}
    #Loop over all frames to find if position changes for each object
    frame_range = bpy.data.scenes["Scene"].frame_end
    for i in range(1, frame_range):
        for name, scene_object in scene_objects_dict.items():   
            #Ignoring Room objects to avoid complications      
            if name == 'Room':
                continue
            #Set move tracker counter to 0 at the first frame
            curr_obj_loc = scene_object.get_location(i)
            prev_obj_loc = scene_object.get_location(i-1)
            if name not in move_change_counter:
                move_change_counter[name] = 0
            if (curr_obj_loc.x - prev_obj_loc.x != 0) or (curr_obj_loc.y - prev_obj_loc.y != 0) or curr_obj_loc.z - prev_obj_loc.z != 0:
                move_change_counter[name]+= 1
                
    #Loop of objects to check if position changes for more than 90% of the total no. of frames
    energy_generated = 0
    energy_saved = 0
    for name, move_duration in move_change_counter.items():
       
       scene_object = scene_objects_dict.get(name, None)
       if move_duration == 0:
          #for static objects, calculate max energy saved i.e. if the object moved for the maximum time the other objects moved 
          energy_saved += scene_object._volume * energy_unit * max(move_change_counter.values())
       else:
          energy_generated += scene_object._volume * energy_unit * move_duration
          
    print(f"Energy generated for the scene : {energy_generated}")
    print(f"Energy saved from the scene : {energy_saved}")
    
    if energy_generated > energy_saved:
       print("It is a joke")
    else:
       print("It is not a joke")   
    print("Finished analysing scene")
    
        
#################### code to play animation #######################################################################
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    count = 0
    
    def modal(self, context, event):
   
        if event.type in {'ESC'} or (bpy.data.scenes["Scene"].frame_current == bpy.data.scenes["Scene"].frame_end):
            self.cancel(context)
            analyse_scene()
            return {'CANCELLED'}

        if event.type == 'TIMER':
            self.count += 1

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_start
        # start animating
        bpy.ops.screen.animation_play()
        self._timer = wm.event_timer_add(1, window=context.window)
        self.count = 0
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.ops.screen.animation_cancel(restore_frame=False)


        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.app.handlers.frame_change_post.append(process_obj_location)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)

####################################################################################################################



set_scene_properties()

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()

    
    
    
