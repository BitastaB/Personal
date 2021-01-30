import bpy
from mathutils import *
import numpy as np  
###############################################################################################################
#                               Generate a simple ladder                                                      #
###############################################################################################################
def generate_ladder(loc_x, loc_y, loc_z):
    
    print("... Generating ladder ...")
    collection = bpy.data.collections.new("Ladder")

    bpy.ops.mesh.primitive_cylinder_add(scale = (0.072, 0.072, 4.606), location = (loc_x, loc_y, loc_z))
    bpy.context.active_object.name = 'ladder_left'
    left_ladder_location = bpy.data.objects['ladder_left'].location
    bpy.data.collections['Ladder'].objects.link(bpy.data.objects['ladder_left'])

    right_ladderlocation = left_ladder_location + Vector((0.8, 0.0, 0.0))
    bpy.ops.mesh.primitive_cylinder_add(scale = (0.072, 0.072, 4.606),location = right_ladderlocation)
    bpy.context.active_object.name = 'ladder_right'
    bpy.data.collections['Ladder'].objects.link(bpy.data.objects['ladder_right'])

    ## generating the steps of the ladder
    ladder_step_loc_x = ((right_ladderlocation[0] - left_ladder_location[0])/2) + left_ladder_location[0]
    print("THE LOC IS : ",ladder_step_loc_x)
    middle_paddle_location = Vector((ladder_step_loc_x, 0, 0))
    i = 0.0
    for x in range(11):
        bpy.ops.mesh.primitive_cylinder_add(location = middle_paddle_location + Vector((0.0, 0.0, i)), rotation = (0, 90*np.pi/180, 0), scale = (0.072, 0.072, 0.829))
        i = i+0.4
        bpy.data.collections['Ladder'].objects.link(bpy.context.active_object)

    print("... Ladder generation complete ...")
    return bpy.data.collections['Ladder']
    #for obj in bpy.data.collections['Ladder'].all_objects:
    #   obj.select_set(True)
    
    
    
    
###############################################################################################################
#                          Generate a simple table                                                            #
###############################################################################################################
def generate_table(loc_x, loc_y, loc_z):
    
    print("... Generating table ...")
    collection = bpy.data.collections.new("Table")
    bpy.ops.mesh.primitive_cube_add(scale = (2, 2, 0.13), location = (loc_x, loc_y, loc_z))
    bpy.data.collections['Table'].objects.link(bpy.context.active_object)
    bpy.context.active_object.name = 'table_top'
    table_top_loc_x = bpy.data.objects['table_top'].location[0]
    table_top_loc_y = bpy.data.objects['table_top'].location[1]
    
    bpy.ops.mesh.primitive_cylinder_add(scale = (0.15, 0.15, 2), location = (table_top_loc_x + 0.5, table_top_loc_y + 0.5, 1))
    bpy.data.collections['Table'].objects.link(bpy.context.active_object)
    
    bpy.ops.mesh.primitive_cylinder_add(scale = (0.15, 0.15, 2), location = (table_top_loc_x - 0.5, table_top_loc_y + 0.5, 1))
    bpy.data.collections['Table'].objects.link(bpy.context.active_object)
    
    bpy.ops.mesh.primitive_cylinder_add(scale = (0.15, 0.15, 2), location = (table_top_loc_x - 0.5, table_top_loc_y - 0.5, 1))
    bpy.data.collections['Table'].objects.link(bpy.context.active_object)
    
    bpy.ops.mesh.primitive_cylinder_add(scale = (0.15, 0.15, 2), location = (table_top_loc_x + 0.5, table_top_loc_y - 0.5, 1))
    bpy.data.collections['Table'].objects.link(bpy.context.active_object)
    
    print("... Table generation complete ...")
    return bpy.data.collections['Table']


################################################################################################################
#                     Generate a simple laptop                                                                 #
################################################################################################################

def generate_laptop(loc_base_x, loc_base_y, loc_base_z):
    print("... Generating laptop ...")

    collection = bpy.data.collections.new("Laptop")

    scale_x = 0.7
    scale_y = 0.6
    scale_z = 0.04


    #keyboard as base
    bpy.ops.mesh.primitive_cube_add(scale = (scale_x, scale_y, scale_z), location = (loc_base_x, loc_base_y, loc_base_z))
    bpy.context.active_object.name = 'keyboard'
    bpy.data.collections['Laptop'].objects.link(bpy.data.objects['keyboard'])

    #screen
    screen_loc_x = loc_base_x
    screen_loc_y = loc_base_y + scale_y/1.3
    screen_loc_z = loc_base_z + (scale_y/2.3)
    bpy.ops.mesh.primitive_cube_add(scale = (scale_x, scale_y, scale_z), location = (screen_loc_x, screen_loc_y, screen_loc_z), rotation = (60  * np.pi /180, 0, 0))
    bpy.context.active_object.name = 'screen'
    bpy.data.collections['Laptop'].objects.link(bpy.data.objects['screen'])
    
    #bpy.data.objects['screen'].parent = bpy.data.objects['keyboard']

    print("... Laptop generation completed ...")
    return bpy.data.collections['Laptop']


################################################################################################################
#                     Generate a simple Pinnochio male                                                                #
################################################################################################################

def generate_pinnochio_male(body_loc_x, body_loc_y, body_loc_z):         
         
    print("\n... Generating pinnochio-male ...")
    collection = bpy.data.collections.new("Pinnochio")

    ##Body 
    #Body loc z recommended to be 1.5

    body_scale_x = 0.65
    body_scale_y = 0.65
    body_scale_z = 1.5
    bpy.ops.mesh.primitive_cylinder_add(scale = (body_scale_x, body_scale_y, body_scale_z), location = (body_loc_x, body_loc_y, body_loc_z))
    bpy.context.active_object.name = 'body'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['body'])


    ##Legs
    leg_scale_x = 0.17
    leg_scale_y = 0.17
    leg_scale_z = 1.2

    leg1_loc_x = body_loc_x - body_scale_x/3
    leg1_loc_y = body_loc_y
    leg1_loc_z = body_loc_z - (body_scale_z/2) - (leg_scale_z/2)
    bpy.ops.mesh.primitive_cylinder_add(scale = (leg_scale_x, leg_scale_y, leg_scale_z), location = (leg1_loc_x, leg1_loc_y, leg1_loc_z))
    bpy.context.active_object.name = 'leg1'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['leg1'])


    leg2_loc_x = body_loc_x + body_scale_x/3
    leg2_loc_y = body_loc_y
    leg2_loc_z = body_loc_z - (body_scale_z/2) - (leg_scale_z/2)
    bpy.ops.mesh.primitive_cylinder_add(scale = (leg_scale_x, leg_scale_y, leg_scale_z), location = (leg2_loc_x, leg2_loc_y, leg2_loc_z))
    bpy.context.active_object.name = 'leg2'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['leg2'])



    #Foot
    foot_scale_x = 0.32
    foot_scale_y = 0.32
    foot_scale_z = 0.07

    feet1_loc_x = leg1_loc_x
    feet1_loc_y = leg1_loc_y
    feet1_loc_z = leg1_loc_z - (leg_scale_z/2) - (foot_scale_z/2)
    bpy.ops.mesh.primitive_cube_add(scale = (foot_scale_x, foot_scale_y, foot_scale_z), location = (feet1_loc_x, feet1_loc_y, feet1_loc_z))
    bpy.context.active_object.name = 'feet1'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['feet1'])

    feet2_loc_x = leg2_loc_x
    feet2_loc_y = leg2_loc_y
    feet2_loc_z = leg2_loc_z - (leg_scale_z/2) - (foot_scale_z/2)
    bpy.ops.mesh.primitive_cube_add(scale = (foot_scale_x, foot_scale_y, foot_scale_z), location = (feet2_loc_x, feet2_loc_y, feet2_loc_z))
    bpy.context.active_object.name = 'feet2'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['feet2'])




    #Neck
    neck_scale_x = 0.17
    neck_scale_y = 0.17
    neck_scale_z = 0.45
    neck_loc_x = body_loc_x
    neck_loc_y = body_loc_y
    neck_loc_z = body_loc_z + (body_scale_z/2) + (neck_scale_z/2)

    bpy.ops.mesh.primitive_cylinder_add(scale = (neck_scale_x, neck_scale_y, neck_scale_z), location = (neck_loc_x, neck_loc_y, neck_loc_z))
    bpy.context.active_object.name = 'neck'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['neck'])


    #Head
    head_scale_x=0.75
    head_scale_y=0.75
    head_scale_z=0.75

    head_loc_x = neck_loc_x
    head_loc_y = neck_loc_y
    head_loc_z = neck_loc_z + (neck_scale_z/2) + (head_scale_z/2)

    bpy.ops.mesh.primitive_uv_sphere_add(scale = (head_scale_x, head_scale_y, head_scale_z), location = (head_loc_x, head_loc_y, head_loc_z))
    bpy.context.active_object.name = 'head'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['head'])


    #Arms
    arm_scale_x=0.17
    arm_scale_y=0.17
    arm_scale_z=1.0

    arm1_loc_x = body_loc_x - (body_scale_x/1.3)
    arm1_loc_y = body_loc_y
    arm1_loc_z = body_loc_z + ((body_scale_z - arm_scale_z)/2)

    bpy.ops.mesh.primitive_cylinder_add(scale = (arm_scale_x, arm_scale_y, arm_scale_z), location = (arm1_loc_x, arm1_loc_y, arm1_loc_z), rotation = (0, 30*np.pi /180, 0))
    bpy.context.active_object.name = 'arm1'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['arm1'])


    arm2_loc_x = body_loc_x + (body_scale_x/1.3)
    arm2_loc_y = body_loc_y
    arm2_loc_z = body_loc_z + ((body_scale_z - arm_scale_z)/2)

    bpy.ops.mesh.primitive_cylinder_add(scale = (arm_scale_x, arm_scale_y, arm_scale_z), location = (arm2_loc_x, arm2_loc_y, arm2_loc_z), rotation = (0, -30*np.pi /180, 0))
    bpy.context.active_object.name = 'arm2'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['arm2'])


    #Hands
    hand_scale_x=0.25
    hand_scale_y=0.25
    hand_scale_z=0.25

    hand1_loc_x = arm1_loc_x - arm_scale_x/0.8
    hand1_loc_y = arm1_loc_y  
    hand1_loc_z = arm1_loc_z - arm_scale_z/2.7
    bpy.ops.mesh.primitive_uv_sphere_add(scale = (hand_scale_x, hand_scale_y, hand_scale_z), location = (hand1_loc_x, hand1_loc_y, hand1_loc_z))
    bpy.context.active_object.name = 'hand1'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['hand1'])

    hand2_loc_x = arm2_loc_x + arm_scale_x/0.8
    hand2_loc_y = arm2_loc_y  
    hand2_loc_z = arm2_loc_z - arm_scale_z/2.7
    bpy.ops.mesh.primitive_uv_sphere_add(scale = (hand_scale_x, hand_scale_y, hand_scale_z), location = (hand2_loc_x, hand2_loc_y, hand2_loc_z))
    bpy.context.active_object.name = 'hand2'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['hand2'])




    #Nose
    nose_scale_x = 0.13
    nose_scale_y = 0.13
    nose_scale_z = 0.40

    nose_loc_x = head_loc_x
    nose_loc_y = head_loc_y - (head_scale_y/2)
    nose_loc_z = head_loc_z

    bpy.ops.mesh.primitive_cylinder_add(scale = (nose_scale_x, nose_scale_y, nose_scale_z), location = (nose_loc_x, nose_loc_y, nose_loc_z), rotation = (90*np.pi /180, 0, 0))
    bpy.context.active_object.name = 'nose'
    bpy.data.collections['Pinnochio'].objects.link(bpy.data.objects['nose'])
    
    
    print("... Male pinnochio generation completed ...")
    return bpy.data.collections['Pinnochio']



################################################################################################################
#                     End of simple Pinnochio male                                                                #
################################################################################################################
