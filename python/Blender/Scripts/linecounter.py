import os
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


Directories = os.listdir("Users/michaelruggiero/Desktop/Samples")

for ChipFolder in Directories:
    if ChipFolder[0] != ".":
        ChipNameList = open("/Users/michaelruggiero/Desktop/ChipNameList.txt", "a")
        ChipFolder = ChipFolder.strip("\n")
        ChipList = os.listdir("Users/michaelruggiero/Desktop/Samples/" + ChipFolder)[0]
        EachChipFile = open("Users/michaelruggiero/Desktop/Samples/" + ChipFolder + "/" + ChipList, "r")
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.delete(use_global=True)
        bpy.ops.import_scene.fbx(filepath="/Users/michaelruggiero/Desktop/reintroductions/Template.fbx", axis_forward='-Z', axis_up='Y')
        ChipNameList.write("\n" + "New Stack # " + ChipFolder + " imported on " + str(datetime.datetime.now()) )
        ChipList = []
        for line in EachChipFile:
            line = line.strip("\n")
            line = line.replace("_", "")
            if line not in ChipList:
                ChipList.append(line)
                ChipNameList.write("\n" + line)
                bring_in(line)
            else:
                line = line.strip(".stl") + "-1.stl"
                if line not in ChipList:
                    ChipList.append(line)
                    ChipNameList.write("\n" + line)
                    bring_in(line)
                else:
                    line = line.strip(".stl") + "-1.stl"
                    if line not in ChipList:
                        ChipList.append(line)
                        ChipNameList.write("\n" + line)
                        bring_in(line)
                    else:
                        line = line.strip(".stl") + "-1.stl"
                        ChipList.append(line)
                        ChipNameList.write("\n" + line)
                        bring_in(line)
        argv = sys.argv
        fbx_out = argv[0]
        bpy.ops.export_scene.fbx(filepath="/Users/michaelruggiero/Desktop/FBX-for-Import/" + ChipFolder +  ".fbx", axis_forward='-Z', axis_up='Y')
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.delete(use_global=True)
        ChipNameList.close()


# for i in range(1000,1002):
#     bpy.ops.object.select_all(action='TOGGLE')
#     bpy.ops.object.delete(use_global=True)
#     bpy.ops.import_scene.fbx(filepath="/Users/michaelruggiero/Desktop/reintroductions/Template.fbx", axis_forward='-Z', axis_up='Y')
#     ChipList = []
#     count = 1
#     ChipNameList.write("\n" + "New Stack # " + str(i) + " imported on " + str(datetime.datetime.now()) )
#     while count < 151:
#         NewChip = random.choice(os.listdir("/Users/michaelruggiero/Desktop/BucketofSTLs/"))
#         if not (NewChip in ChipList):
#             ChipList.append(NewChip)
#             ChipNameList.write("\n" + NewChip)
#             count += 1
#             print(NewChip)
#             bring_in(NewChip)
#         else:
#             print("Nope")
#     argv = sys.argv
#     # argv = argv[argv.index("--") + 1:] # get all args after "--"
#     fbx_out = argv[0]
#     bpy.ops.export_scene.fbx(filepath="/Users/michaelruggiero/Desktop/FBX-for-Import/" + str(i) + "/" + str(i) + ".fbx", axis_forward='-Z', axis_up='Y')
#     bpy.ops.object.select_all(action='TOGGLE')
#     bpy.ops.object.delete(use_global=True)
#
# ChipNameList.close()
