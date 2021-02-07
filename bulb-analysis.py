import bpy

print("Starting...")

scene_objects_list = []
frame_read_counter = []

class SceneObject:
  
  def __init__(self, name):
      print(f"Initialising {name}")
      self.name = name 
      self._location = []
      print("initalisation complete")
    
  @property
  def location(self):
      """I'm the location of the scene object."""
      print(f"getter of location called for {self.name}")
      return self._location

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
        so.set_location(i)
        so.set_location(i*5)
        i+=1
        scene_objects_list.append(so)         
        print("added loc :"+ str((so.location)[1]))
      #  print("test get by name : "+ str(so.getByName(obj.name).loc[0]))
        print(f"Setting params completed for {obj.name}\n")
        
    for object in scene_objects_list:
        if(object.name == 'Ladder'):
            print("Testing accessing object locations"+ str(object.location[0]))     
        
    print("Total objects in current scene : " + str(len(scene_objects_list)))
                  
                
def process_obj_location(self):
    current_frame = bpy.data.scenes["Scene"].frame_current
    print(f"Processing object location for frame {current_frame}")    
    if (current_frame in frame_read_counter):
        return
    frame_read_counter.append(bpy.data.scenes["Scene"].frame_current)
    print(f"Finished processing locations for frame : {current_frame}")
    
    
#################### code to play animation #######################################################################
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    count = 0
    
    def modal(self, context, event):
        process_obj_location(self)
        if event.type in {'ESC'} or (bpy.data.scenes["Scene"].frame_current == bpy.data.scenes["Scene"].frame_end):
            self.cancel(context)
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
    
