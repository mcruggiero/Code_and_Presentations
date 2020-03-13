# i = 1
# j = 0
import os, random
import bpy
import sys
import datetime

ChipNameList = open("/Users/michaelruggiero/Desktop/ChipNameList.txt", "a")
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)

def bring_in(filename):
    # try:
    bpy.ops.import_mesh.stl(filepath="/Users/michaelruggiero/Desktop/BucketofSTLs/" + filename)
    objects = bpy.data.objects
    print(objects)
    a = objects['0']
    b = objects[filename.split(".")[0]]
    b.parent = a
    bpy.context.object.scale[0] = .1
    bpy.context.object.scale[1] = .1
    bpy.context.object.scale[2] = .1
        #bpy.ops.transform.translate(value=( 0, -0.41 - i*.0001, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size = 1, release_confirm=False)
    # except:
    #     os.remove("/Users/michaelruggiero/Desktop/BucketofSTLs/" + filename)
    #     print("/Users/michaelruggiero/Desktop/BucketofSTLs/" + filename + " Removed")
    #     pass

for i in range(3021,3101):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=True)
    bpy.ops.import_scene.fbx(filepath="/Users/michaelruggiero/Desktop/reintroductions/Template.fbx", axis_forward='-Z', axis_up='Y')
    ChipList = []
    count = 1
    ChipNameList.write("\n" + "New Stack # " + str(i) + " imported on " + str(datetime.datetime.now()) )
    while count < 121:
        NewChip = random.choice(os.listdir("/Users/michaelruggiero/Desktop/BucketofSTLs/"))
        if not (NewChip in ChipList):
            ChipList.append(NewChip)
            ChipNameList.write("\n" + NewChip)
            count += 1
            print(NewChip)
            bring_in(NewChip)
        else:
            print("Nope")
    argv = sys.argv
    # argv = argv[argv.index("--") + 1:] # get all args after "--"
    fbx_out = argv[0]
    bpy.ops.export_scene.fbx(filepath="/Users/michaelruggiero/Desktop/FBX-for-Import/" + str(i) + "/" + str(i) + ".fbx", axis_forward='-Z', axis_up='Y')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=True)

ChipNameList.close()
