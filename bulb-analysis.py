import bpy
from bpy.app.handlers import persistent

print("Starting...")

frame_read_counter = []
scene_objects_dict = {}

class SceneObject:
  
  def __init__(self, name):
      print(f"Initialising {name}")
      self.name = name 
      self._location = []
      print("initalisation complete")
    
 # @property
  def get_location(self,i):
      """I'm the location of the scene object."""
      print(f"getter of location called for {self.name} for frame {i}")
      return self._location[i]

 # @loc.setter
  def set_location(self, loc):
      print(f"setter of location called for {self.name}")
   #   print("Length of frame_and_loc: "+ str(len(frame_and_loc)))
    #  print("frame no.: "+ str(frame_and_loc[0]))
    #  print("location of object : "+ str(frame_and_loc[1]))
    #  self._loc.insert(frame_and_loc[0], frame_and_loc[1])
      self._location.append(loc) 
      
      
  def get_by_name(self, name):
      if(self.name == name):
          return self     
    


############ Set global scene properties 
def set_scene_properties():
    
    i=100
    print("Setting scene properties")
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH': 
        so = SceneObject(obj.name)
        print("added object : "+so.name)
        scene_objects_dict[obj.name] = so
        print(f"Setting params completed for {obj.name}\n")
        
    print("Total objects in current scene : " + str(len(scene_objects_dict)))
                  
########### Process location/rotation of objects during animation 
               
def process_obj_location(scene):
    print("HAHAHAHAHAAHAHAHA")
    if scene.frame_current in frame_read_counter:
        return
    print(f"Processing object location for frame : {str(scene.frame_current)}")   
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH': 
          location = obj.rotation_euler
          object_instance = scene_objects_dict.get(obj.name, None)
          object_instance.set_location(location)
    
    frame_read_counter.append(scene.frame_current)
    print(f"Finished processing locations for frame {str(scene.frame_current)}")


 
########## Analyse object movement post animation   
def analyse_scene():
    print("Animation over, will analyse scene now")
    ladder_object = scene_objects_dict.get("Ladder")
    print("Testing accessing Ladder locations 0 : "+ str(ladder_object.get_location(0)) + " 50 : "+str(ladder_object.get_location(50)))  
    p_object = scene_objects_dict.get("Pinnochio")
    print("Testing accessing Pinnochio locations 0 : "+ str(p_object.get_location(0)) + " 50 : "+str(p_object.get_location(50)))  

    
        
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


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)

####################################################################################################################



set_scene_properties()

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
    bpy.app.handlers.frame_change_post.append(process_obj_location)
    
