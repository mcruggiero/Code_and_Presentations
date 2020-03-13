i = 1
j = 0
import os

def bring_in(filename):
    try:
        bpy.ops.import_mesh.stl(filepath="/Users/michaelruggiero/Desktop/001/" + filename)
        bpy.data.objects[filename].select = True
        bpy.data.objects['0'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['0']
        bpy.ops.object.parent_set()
        a = objects['0']
        b = objects[filename]
        b.parent = a
        bpy.context.object.scale[0] = .1
        bpy.context.object.scale[1] = .1
        bpy.context.object.scale[2] = .1
        #bpy.ops.transform.translate(value=( 0, -0.41 - i*.0001, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size = 1, release_confirm=False)
    except:
        print(" \n you fail!")
        pass

for f in os.listdir("/Users/michaelruggiero/Desktop/001/"):
    if j < 10:
        if not f.startswith('.'):
            bring_in(f)
            i += 1
            j += 1
