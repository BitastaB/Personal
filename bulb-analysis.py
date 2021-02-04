import bpy

print("Starting...")

sceneObjects = []
frameEnd = 0

### set global scene properties
def setSceneProperties():
    
    print("Retrieving scene properties")
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH':          
          sceneObjects.append(obj.name)
    if 'Room' in sceneObjects:
        sceneObjects.remove('Room')
    print("Total objects in current scene : " + str(len(sceneObjects)))
    print(f'Objects in scene are {sceneObjects}')
    
    frameEnd = bpy.data.scenes["Scene"].frame_end
    
def analyse_scene1():
    objectCount = 0 
    print("Objects in the scene are :")
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH':          
          objectCount+=1
          print(obj.name)
          anim = obj.animation_data
          if anim is not None and anim.action is not None:
              for fcu in anim.action.fcurves:
                  print("keyframe length thingy: "+str(len(fcu.keyframe_points)))
                  

#################### code to play animation #######################################################################
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    count = 0
    
    def modal(self, context, event):
        #print("in modal: stopAnimation "+str(stopAnimation))
        #evaluateScene()
        if event.type in {'ESC'} or (bpy.data.scenes["Scene"].frame_current == bpy.data.scenes["Scene"].frame_end):
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            self.count += 1


        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        # start animating
        bpy.ops.screen.animation_play()
       # analyse_scene()
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



setSceneProperties()

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
    
