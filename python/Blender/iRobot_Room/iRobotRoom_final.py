###
# Interview Homework for 3D Programmer
# Completed By: Michael Ruggiero
# Due Date: April 2nd, 9am
###

###
# Instructions
###
#
#     • In the Models folder, there are 4 assets: a coffee table, a sofa,
#       a chair and a wall clock. All assets are in Blender 2.81
#     • You need to create a class using the Blender API in python.
#       The class should have a method for each of the following actions:
#         ◦ [TASK 1] Create a new scene.
#         ◦ [TASK 2] Create a room.
#         ◦ [TASK 3] Place in a random position a table, a sofa, two chairs
#           and a wall clock inside the room. The position of the
#           furniture should be random, but considering the following constraints:
#             ▪ The sofa should be close to a wall.
#             ▪ The coffee table should be near to the center of the room.
#             ▪ The chairs should be close to the table.
#             ▪ The wall clock should be against a wall.
#         ◦ [TASK 4] Add lights to the scene.
#         ◦ [TASK 5] Save the scene.
#     • [TASK 6] At the end of the class there should be a main function that allows
#       to run the script in the command line.
#     • To deliver the homework, please send us a single .py file.
#
#
# Optional tasks:
#     • [TASK 7] Create a method for configuring a camera and setting
#       the parameters for rendering.
#     • [TASK 8] Create a method for rendering an image.
###

###
# Important Tl;dr: Please change path to your folder below into the Main
# class on if __name__== "__main__" before running
###

###
# General Notes:
#
# The general idea behind this work is to break up the Main class into
# smaller functional classes, such as Sofa, where most of the work of that
# object is accomplished. This style helped keep everything somewhat organized and
# readable (for me at least), but I could have easily used a Functional tact and
# made one Main class with all of the funcitons inside. I know a lot of shade
# is being thrown at OOP right now, but for this particular problem, it helped me.
# Anyway, the instructions seemed to grant me a lot of flexibility, so
# when I came to a major decision in the code (for example how near the table
# is to the center, or the dimensions of the room) I tried to comment out the
# decsion nodes clearly. Finally, I relied a little too much on
# ".ops" to save on time. A lot has changed since blender 2.6
# and with the tight schedule, I needed to cut my learning curve.
# Obviously this code is not intended for production.
#
# Happy to answer any questions you have about the project. Thanks again for
# opportunity to see your iRobot/Blender pipeline. All tasks completed.
#
# ~Michael
##


import bpy
import bmesh
import os
# Don't need numpy and re, but they are nice to have in the toolbox
import numpy as np
import re
from datetime import datetime
from mathutils import Vector, Euler

class Main:
    def __init__(self, path):
        #Starting in object mode fixed some bugs I was having with the script
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        now = datetime.now().isoformat(timespec='minutes')
        print("\n *** New Simulation Running at Time {} ***".format(now))
        self.now    = now
        self.path   = path
        self.room   = self.Room(self.path)
        self.table  = self.Table(self.path,
                                 self.room.middle)

        self.chairs = self.Chairs(self.path,
                                  self.table.away_from_middle)

        self.sofa   = self.Sofa(self.path,
                                self.room.x_dim,
                                self.room.y_dim)

        self.clock  = self.Clock(self.path,
                                 self.room.x_dim,
                                 self.room.y_dim)

        self.lights = self.Lights(self.table.away_from_middle,
                                  self.room.x_dim,
                                  self.room.y_dim)

        self.camera = self.Camera(self.path,
                                  self.now,
                                  self.room.x_dim,
                                  self.room.y_dim)

        ###
        #Task 5
        ###

        print("Making .blend file of scene at {}".format(self.path + "_iRobot_Room_{}.blend".format(now)))
        bpy.ops.wm.save_as_mainfile(filepath= self.path + "_iRobot_Room_{}.blend".format(now))


    class Room:
        def __init__(self, path):
            self.path   = path
            self.scene  = self.clean_space()

            # set dimensions of room, measurements in meters
            self.x_min  = 4
            self.x_max  = 6
            self.y_min  = 4
            self.y_max  = 6

            ###
            # *Three Wall Decision*
            # Using only 3 walls, one open for camera, other options are
            # programatically possible.
            ###

            # The dimensions are randomly generated from min and max above.
            self.x_dim  = np.random.uniform(low = self.x_min,
                                            high= self.x_max,
                                            size= None)
            self.y_dim  = np.random.uniform(low = self.x_min,
                                            high= self.x_max,
                                            size= None)
            # Set the space
            self.middle = self.make_space(self.x_dim, self.y_dim)

        def clean_space(self):
            print("Cleaning room")
            # clean Space
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)

            ####
            # *Deleting Older Scenes Decision*
            # Not sure if you want to keep older scenes for analysis
            # or if you want only one scene for every simulation.
            # I will not keep old scenes let me know if that doesn't work.
            ###

            if "Room Scene" in bpy.data.scenes.keys():
                bpy.data.scenes.remove(bpy.data.scenes["Room Scene"])

            # Rushed this scene naming convention and just called it whenever
            # I needed it.
            room_scene = bpy.data.scenes.new(name='Room Scene')
            bpy.context.window.scene = room_scene
            #bpy.context.scene.background_set = bpy.data.scenes["Room Scene"]

            return room_scene

            ###
            # Task 1 complete
            ###

        def make_space(self, x_dim, y_dim):
            # Print report
            print("Making {}m X {}m floor".format(x_dim, y_dim))

            # Make cube mesh
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True, location=(1, 1, 1))
            bpy.data.objects['Cube'].name = 'Room'
            bpy.data.objects['Room'].data.name = 'Room'

            # Move faces to match dimensions
            bpy.ops.mesh.select_all(action = "DESELECT")
            bm = bmesh.from_edit_mesh(bpy.data.objects["Room"].data)
            bm.faces.ensure_lookup_table()
            room_object = bpy.data.objects["Room"]

            ###
            # *Face Labeling Decision*
            # I knew the faces and labeling through trial and error, which
            # according to "The Blender Python API" page 34, is "an acceptable practice"
            # if time was a little less tight, however, I would add a few lines locating the faces
            # more programatically. Face labeling can change with version. Repay technical debt later and
            # scrub out all of these ".ops"
            ###

            # Set room dimensions along x axis
            bm.faces[2].select = True
            bpy.ops.transform.translate(value = (x_dim - 2, 0, 0))
            bpy.ops.mesh.select_all(action = "DESELECT")

            # Set room dimensions along y axis
            bm.faces[1].select = True
            bpy.ops.transform.translate(value = (0, y_dim - 2, 0))
            bpy.ops.mesh.select_all(action = "DESELECT")

            # Set room dimensions along z axis, set to standard ceiling height of 2.7m
            bm.faces[5].select = True
            bpy.ops.transform.translate(value = (0, 0, .7))

            # Remove ceiling and break fourth wall
            bm.faces[1].select = True
            bpy.ops.mesh.delete(type='FACE')
            bpy.ops.mesh.select_all(action = "DESELECT")

            # We will be some of the subdivisions for placement vertices
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.subdivide(number_cuts=1)
            bpy.ops.mesh.select_all(action = "DESELECT")

            # Apply all transforms to make verts easier to locate later
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)

            # Find middle of floor, here too many points to scan through, will us programatic solutlion
            for vertex in room_object.data.vertices.items():

                #Check to see that x and y are in the middle with z on floor
                if (0 < vertex[1].co[0] < np.floor(x_dim) and # floor removes rounding errors
                    0 < vertex[1].co[1] < np.floor(y_dim) and
                    vertex[1].co[2] == 0):
                    print("Middle of the floor is at {}".format(vertex[1].co))
                    middle = vertex[1], vertex[1].co

            return middle

    class Table:

        ###
        # *Table/chair Roation Decision*
        # There is an intersting problem here, Tables are often oriented to
        # the wall space, but not always. For this simulation, I will assume
        # that the table plane is oriented parallel to the walls and the chairs
        # are oriented along the short side across from each other, rather than
        # sloppily set nearby the table. While this satisfies your conditions,
        # I hope this strategy works for the team. Setting a more random orientation
        # is not a problem, and if you like I can change the simulation to fit your needs.
        ###

        def __init__(self, path, middle):
            self.path = path + "/table.blend/Object"
            # The dimensions are randomly generated between -.5 and .5 meters
            x_random  = np.random.uniform(low  = -.4,
                                          high =  .4)

            y_random  = np.random.uniform(low  = -.4,
                                          high =  .4)

            self.away_from_middle = middle[1] + Vector((x_random, y_random, -.05))
            print("Making Table at Location: {}".format(self.away_from_middle))
            self.generate_table(self.away_from_middle, self.path)

        def generate_table(self, away_from_middle, path):

            ###
            # *Removing Plane Decision*
            # I didn't realize that there were extra objects inside of table when
            # I started programing. For now, I don't think you want the plane as
            # lighting rigging, so I'm going to leave it out of the simulation,
            # please let me know if that doesn't work. It is a trivial modification.
            ###

            bpy.ops.wm.append(directory = path,
                              filepath  = "table.blend",
                              filename  = "table")

            room_scene = bpy.context.scene
            for obj in room_scene.objects:
                if obj.name[:5] == "Plane":
                    print("Removing {}".format(obj.name))
                    bpy.data.objects[obj.name].select_set(True)
                else:
                    bpy.data.objects[obj.name].select_set(False)

            # Once the Plane is identified we can delete
            bpy.ops.object.delete(use_global=False)

            # Select Table and move it to away_from_middle
            bpy.context.scene.objects["table"].select_set(True)
            bpy.ops.transform.translate(value=away_from_middle,
                                        orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL',
                                        release_confirm=True)

    class Chairs:
        def __init__(self, path, away_from_middle):
            self.path = path + "/chair.blend/Object"
            self.away_from_middle = away_from_middle
            self.generate_chairs(self.path, self.away_from_middle)

        def generate_chairs(self, path, away_from_middle):
            bpy.ops.wm.append(directory= path,
                              filepath="chair.blend",
                              filename = "chair")

            # Move chair across from Table, .75 m away from center
            print("Making Chairs at {} and {}".format(away_from_middle + Vector((.75,0,0)),
                                                      away_from_middle - Vector((.75,0,0))))

            bpy.ops.transform.translate(value=away_from_middle + Vector((.75,0, -.05)),
                                        orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL',
                                        release_confirm=True)

            # Duplicate chair, set it across, and rotate it
            # So many options here are required to do this move and duplicate at once.
            # Will clean up this inelegant code if I have time.
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                                          TRANSFORM_OT_translate={"value":(-1.5, 0, 0),
                                                                  "orient_type":'GLOBAL',
                                                                  "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                                                  "orient_matrix_type":'GLOBAL',
                                                                  "constraint_axis":(False, False, False),
                                                                  "mirror":True,
                                                                  "use_proportional_edit":False,
                                                                  "proportional_edit_falloff":'SMOOTH',
                                                                  "proportional_size":1,
                                                                  "use_proportional_connected":False,
                                                                  "use_proportional_projected":False,
                                                                  "snap":False,
                                                                  "snap_target":'CLOSEST',
                                                                  "snap_point":(0, 0, 0),
                                                                  "snap_align":False,
                                                                  "snap_normal":(0, 0, 0),
                                                                  "gpencil_strokes":False,
                                                                  "cursor_transform":False,
                                                                  "texture_space":False,
                                                                  "remove_on_cancel":False,
                                                                  "release_confirm":False,
                                                                  "use_accurate":False})

            bpy.ops.transform.rotate(value=np.pi,
                                     orient_axis='Z',
                                     orient_type='GLOBAL',
                                     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                     orient_matrix_type='GLOBAL')

    class Sofa:

        ###
        # *Sofa Decision*
        # Here we have a corner sofa and some considerations need to be made
        # to make the simulation realistic. First, I will make the long
        # edge against one of the walls. Next, we need to keep the
        # short edge away from the table. Finally, we need to keep the Sofa
        # in the room completely. The width of object center to edge is almost 1 meter,
        # which is actually rather large for the room space. Therefore, I will
        # randomly assign the corner sofa to one of the corners. This solutlion
        # is perhaps not ideal and I actually did a lot of "corner sofa" research.
        # In some circles it is trendy to not put the corner sofa in the corner,
        # but this decorating decsion is often made in rooms larger than this. Since
        # we are also missing a wall for the camera, that leaves two possible corners.
        ###

        ###
        # *Wall Direction Decision*
        # North points to the empty wall
        ###

        def __init__(self, path, x_dim, y_dim):
            self.path = path + "/sofa.blend/Object"
            self.x_dim = x_dim
            self.generate_sofa(self.path, self.x_dim)

        def generate_sofa(self, path, x_dim):

            bpy.ops.wm.append(directory= path,
                              filepath="sofa.blend",
                              filename = "sofa")

            # Choose one of two random corners to move Sofa
            corner = np.random.choice(["south west", "south east"])

            print("Making sofa in {} corner".format(corner))
            if corner == "south east":
                # Rotate
                bpy.ops.transform.rotate(value=np.pi,
                         orient_axis='Z',
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                         orient_matrix_type='GLOBAL')

                # Place
                bpy.ops.transform.translate(value = Vector((1,1.05,0)),
                            orient_type='GLOBAL',
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            orient_matrix_type='GLOBAL',
                            release_confirm=True)
            else:
                bpy.ops.transform.rotate(value=3/2 * np.pi,
                         orient_axis='Z',
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                         orient_matrix_type='GLOBAL')

                # Place
                bpy.ops.transform.translate(value = Vector((x_dim - 1.1,1.05,0)),
                            orient_type='GLOBAL',
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            orient_matrix_type='GLOBAL',
                            release_confirm=True)

    class Clock:

        ###
        # *Clock Decision*
        # Compaired to the sofa, no questions about position. Just going to
        # keep the clock between 1/2 and 2/3 of total wall height.
        # Also making a margin to keep the clock away from the corner.
        # The weirdness is comming in with the rendering. There is a
        # strange alternate dimension on the opposite side of the clock in a material
        # called "Uhr_2," since it is not a clock related item and it slows down
        # the rendering, I am going to delete the uhr materials.
        ###

        def __init__(self, path, x_dim, y_dim):
            self.path = path + "/wall_clock.blend/Object"
            self.x_dim = x_dim
            self.y_dim = y_dim
            self.generate_clock(self.path,
                                self.x_dim,
                                self.y_dim)

        def generate_clock(self, path, x_dim, y_dim):
            bpy.ops.wm.append(directory= path,
                              filepath="wall_clock.blend",
                              filename = "wall_clock")

            # Remove all of the Uhr_2 weirdness
            bpy.data.objects["wall_clock"].select_set(True)

            for material in bpy.data.materials.keys():
                if material[:4] == "Uhr_":
                    print("removig {} material from clock".format(material))
                    bpy.data.materials.remove(bpy.data.materials[material])

            # Choose which wall for the clock
            wall = np.random.choice(["east", "south","west"])

            # Setting the height between 1.5 and 1.65 meters
            if wall == "east":
                clock_x = x_dim - .05
                clock_y = np.random.uniform(low = 1, high = y_dim - 1)
                clock_z = np.random.uniform(low = 1.5, high =  1.65)
            elif wall == "south":
                clock_x = np.random.uniform(low = 1, high = x_dim - 1)
                clock_y = .05
                clock_z = np.random.uniform(low = 1.5, high =  1.65)

                # This time we need to rotate the clock to match the wall
                bpy.ops.transform.rotate(value = - np.pi / 2,
                         orient_axis='Z',
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                         orient_matrix_type='GLOBAL')
            else:
                clock_x = .05
                clock_y = np.random.uniform(low = 1, high = y_dim - 1)
                clock_z = np.random.uniform(low = 1.5, high =  1.65)

                bpy.ops.transform.rotate(value = np.pi,
                         orient_axis='Z',
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                         orient_matrix_type='GLOBAL')

            # Place clock
            print("Making clock at point: {}, {}, {}".format(clock_x, clock_y, clock_z))
            bpy.ops.transform.translate(value = Vector((clock_x,clock_y,clock_z)),
                        orient_type='GLOBAL',
                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                        orient_matrix_type='GLOBAL',
                        release_confirm=True)

            ###
            # Task 3 Complete
            ###
            print("Scene Completed")

    class Lights:

        ###
        # *Lighting Decision*
        # All that it seems you want from me is to add some lights, Not going
        # to get too creative, but I will still have a little fun in the
        # mode of randomness. Just a simple three point light system
        ###

        def __init__(self, away_from_middle, x_dim, y_dim):
            self.generate_lights(away_from_middle, x_dim, y_dim)

        def generate_lights(self, away_from_middle, x_dim, y_dim):

            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            for i in range(3):
                # Code modifed from stack exchange
                x_light = np.random.uniform(0, x_dim)
                y_light = np.random.uniform(0, y_dim)
                z_light = np.random.uniform(0, 2.7)

                # create light datablock, set attributes
                light_data = bpy.data.lights.new(name="light_{}".format(i), type='POINT')
                light_data.energy = np.random.uniform(0, 100)
                light_data.color = [np.random.uniform() for x in range(3)]

                # create new object with our light datablock
                light_object = bpy.data.objects.new(name="light_{}".format(i), object_data=light_data)

                # link light object
                bpy.context.collection.objects.link(light_object)

                # make it active
                bpy.context.view_layer.objects.active = light_object

                #change location
                light_object.location = (x_light, y_light, z_light)

                bpy.context.evaluated_depsgraph_get().update()
                print("Placing light {} at {}, {}, {}".format(i, x_light, y_light, z_light))

                ###
                # Task 4 Complete
                ###

            print("Scene Lit")

    class Camera:

        ###
        # *Camera Decision*
        # Not getting too fancy on camera, just placing it in the middle.
        ###

        def __init__(self, path, now, x_dim, y_dim):
            self.generate_camera(path, now, x_dim, y_dim)

        def generate_camera(self, path, now, x_dim, y_dim):

            # Create the camera
            room_scene = bpy.context.scene
            camera_data = bpy.data.cameras.new('camera')
            camera = bpy.data.objects.new('camera', camera_data)
            bpy.context.collection.objects.link(camera)
            room_scene.camera = camera

            # make it active
            bpy.context.view_layer.objects.active = camera

            # Putting the camera smack in the middle
            camera_x = x_dim/2
            camera_y = y_dim * 2.5
            camera_z = 2.2

            print("Making camera at {}, {}, {}".format(camera_x, camera_y, camera_z))

            camera.location = Vector((camera_x, camera_y, camera_z))
            # I really should have used Eulers for all of my rotations

            # I am not going to spend a lot of time to calculate the ideal focus and placement
            # of the camera. Added a little angular spice to make the scene visually interesting
            camera.rotation_euler = Euler((3 * np.pi / 2 -.15, np.pi, 0))

            room_scene.render.image_settings.file_format = "PNG"
            room_scene.render.filepath = path + "room_{}.png".format(now)

            print("Taking Picture")
            bpy.ops.render.render(write_still = 1)

            ##
            # Task 7 and 8
            ##

if __name__== "__main__":

    ###
    # Important Note: Change to you folder folder path below.
    ###
    simulation = Main("/home/michael/Desktop/InterviewHomework/Models")  # Task 6
