import bpy
import os
import numpy as np
import csv
from mathutils import Vector
import random as r

def main():
	# Set memory settings
	set_memory_settings()
	# These values will be common to all measurements of bulk density
	jug_name = 'Jug'
	chipStack_name = '0'
	density = 1200 # kg/m^3
	jug_thickness = 0.03 # m
	chip_thickness = 0.0017 # m
	realign_margin = 0.005 # Margin between subdivided chip stacks
	data_dicts = []
	stack_number = 1
	measurement_folder = "chips" # This folder includes several subfolders (one per measurement) that in turn hold unique stacks of chips to be dropped
	measurements_directory = "G:/" + measurement_folder + "/"
	chipStacks_folder_list = os.listdir(measurements_directory)
	# Import and measure one version of the standard jug to be reused for each measurement
	original_jug_bounds = import_jug(jug_name,jug_thickness)
	for chipStack_folder in chipStacks_folder_list: # These are the folders containing several stacks of chips; one folder corresponds to one measurement of bulk density
		if (chipStack_folder != 'ss'):
			chipStacks = os.listdir(measurements_directory + chipStack_folder)
			# Delete leftover scene from previous measurement, reset counters and values
			if stack_number != 1:
				bpy.context.screen.scene = bpy.data.scenes[str(stack_number-1)]
				bpy.ops.scene.delete()
				stack_number = 1
			fill_height = 0
			for file in chipStacks: # These are files containing single stacks of chips
				if (fill_height < 0.1965) and (file != 'ss'): # 0.177 corresponds to 4.0L, 0.1965 would correspond to 4.5L:
					scene_copy(stack_number) # copy most recent file, whether the standard jug or the latest settlement
					scene_delete(stack_number) # delete scenes of old settlements
					jug_rename(stack_number, jug_name) # rename the jug according to the scene number
					manipulate_chip_stack(measurements_directory,chipStack_folder,chipStack_name,file,stack_number,realign_margin,original_jug_bounds,chip_thickness,Vector,jug_thickness,fill_height)
					apply_physics(chip_thickness,stack_number)
					animate(stack_number)
					fill_height = calc_bag_fill(stack_number,jug_thickness,original_jug_bounds) # calculate fill height
					clean_scene(stack_number,original_jug_bounds,fill_height,jug_thickness) # delete chips displaying aphysical behavior
					fill_height = calc_bag_fill(stack_number,jug_thickness,original_jug_bounds) # recalculate fill height
					total_chip_mass = calc_chip_mass(stack_number,density,chip_thickness) # calculate mass of chips
					vol_fill = calc_vol_fill(fill_height) # calculate volume fill from fill height
					bulk_density = calc_bulk_density(total_chip_mass,vol_fill) # calculate bulk density
					settled_chips_rename(stack_number) # rename settled chips to distinguish them from ones to be newly imported
					output_data = [total_chip_mass,fill_height,vol_fill,bulk_density]
					data_dicts = output_data_org(file,output_data,data_dicts)
					stack_number += 1
					csv_writer(csv,os,data_dicts,measurement_folder)
			export_scene(os,measurement_folder,chipStack_folder)
	print('Script finished')

def set_memory_settings():
	bpy.context.user_preferences.edit.use_global_undo = False
	bpy.context.user_preferences.edit.undo_steps = 0
	bpy.context.user_preferences.edit.undo_memory_limit = 0

def import_jug(jug_name,jug_thickness):
	# Import standard jug
	bpy.ops.import_scene.fbx(filepath='G:\')
	item = bpy.data.objects[jug_name]
	bpy.context.scene.objects.active = item
	item.select = True
	# Apply transparency to bag
	item.data.materials[0].use_transparency = True
	item.data.materials[0].alpha = 0.2
	item.show_transparent = True
	# Subdivide mesh to improve volume calculation and add thickness to prevent chips from falling through
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.subdivide(number_cuts = 8, smoothness = 0.0)
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.rigidbody.object_add(type='ACTIVE')
	item.rigid_body.collision_shape = 'MESH'
	item.rigid_body.mesh_source = 'FINAL'
	item.rigid_body.friction, item.rigid_body.restitution, item.rigid_body.collision_margin = 0.850, 0.200, 0.0
	original_jug_bounds = obj_bounds(bpy,Vector,jug_name)
	bpy.ops.object.modifier_add(type='SOLIDIFY')
	bpy.context.object.modifiers['Solidify'].thickness = jug_thickness
	# Lock location of jug to keep it from falling under gravity
	for i in range(3):
		bpy.data.objects[jug_name].lock_location[i] = True
		bpy.data.objects[jug_name].lock_rotation[i] = True
		bpy.data.objects[jug_name].lock_scale[i] = True
	return original_jug_bounds

def scene_copy(stack_number):
	# Copy the results of the previous stack drop into a new scene
	if stack_number == 1:
		bpy.context.screen.scene = bpy.data.scenes['Scene']
	else:
		bpy.context.screen.scene = bpy.data.scenes[str(stack_number-1)]
	bpy.ops.scene.new(type='FULL_COPY')
	active_scene = bpy.context.scene
	active_scene.name = str(stack_number)

def scene_delete(stack_number):
	# Delete the superseded scenes of dropped chip stacks
	if stack_number != 1:
		bpy.context.screen.scene = bpy.data.scenes[str(stack_number-1)]
		bpy.ops.scene.delete()

def jug_rename(stack_number, jug_name):
	# Rename the jug in the most recent scene
	bpy.context.screen.scene = bpy.data.scenes[str(stack_number)]
	if stack_number < 10:
		bpy.data.objects[jug_name+'.00'+str(stack_number)].name = jug_name
	else:
		bpy.data.objects[jug_name+'.0'+str(stack_number)].name = jug_name

def import_chips_fbx(measurements_directory, chipStack_folder, chipStack_name, file, active_scene):
	# Import the unmanipulated stack of chips into an empty scene
	bpy.context.screen.scene = active_scene
	bpy.ops.import_scene.fbx(filepath= measurements_directory + chipStack_folder + '/' + file)
	bpy.ops.transform.rotate(value=2.35619449,constraint_axis=(True,False,False))

def import_chips_cleanup(chipStack_name):
	# Clear parents and delete parent object
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.scene.objects.active = bpy.data.objects[chipStack_name]
	bpy.ops.object.select_hierarchy(direction='CHILD')
	bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
	bpy.ops.object.select_all(action='DESELECT')
	bpy.data.objects[chipStack_name].select = True
	bpy.ops.object.delete()
	# Select all and reset points to their geometries (i.e. realign centers of mass)
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
	# Apply 'Rotation & Scale' transformation
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
	bpy.ops.object.select_all(action='DESELECT')

def stack_bounds(stack_number):
	# Find the bounds of the chip stack in a separate scene, then delete the scene
	scene = bpy.data.scenes[str(stack_number)]
	chipStack_bounds = {'x_low':99999,'x_high':-99999,'y_low':99999,'y_high':-99999,'z_low':99999,'z_high':-99999}
	for item in scene.objects:
		if ("GH_Obj" in item.name) and ('_settled' not in item.name):
			chip_bounds = obj_bounds(bpy,Vector,item.name)
			if chip_bounds['x_low'] < chipStack_bounds['x_low']:
				chipStack_bounds['x_low'] = chip_bounds['x_low']
			if chip_bounds['y_low'] < chipStack_bounds['y_low']:
				chipStack_bounds['y_low'] = chip_bounds['y_low']
			if chip_bounds['z_low'] < chipStack_bounds['z_low']:
				chipStack_bounds['z_low'] = chip_bounds['z_low']
			if chip_bounds['x_high'] > chipStack_bounds['x_high']:
				chipStack_bounds['x_high'] = chip_bounds['x_high']
			if chip_bounds['y_high'] > chipStack_bounds['y_high']:
				chipStack_bounds['y_high'] = chip_bounds['y_high']
			if chip_bounds['z_high'] > chipStack_bounds['z_high']:
				chipStack_bounds['z_high'] = chip_bounds['z_high']
	return chipStack_bounds

def translate(item,vect):
	# Translate a data object by some vector
	item.select = True
	item.location += vect
	item.select = False

def delete_obj(item):
	item.select = True
	bpy.ops.object.delete()

def quad_test(R_minus_m,chip_x_dim,chip_y_dim,x_margin,y_margin,chip_margin):
	# Determine which quadrant the chip center of mass would sit in and what factors are required to properly aim the vector
	if (x_margin + chip_margin + (chip_x_dim/2) >= R_minus_m) and (y_margin + chip_margin + (chip_y_dim/2) <= R_minus_m): # quad I
		q1, q2 = True, False
	elif (x_margin + chip_margin + (chip_x_dim/2) < R_minus_m) and (y_margin + chip_margin + (chip_y_dim/2) <= R_minus_m): # quad II
		q1, q2 = False, True
	else:
		q1, q2 = False, False
	return (q1, q2)

def row_layer_filter(i, Vector, q1, q2, new_layer_bool, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner):
	sqrt = 0
	# Determine if the chip will fit on the current row or the next row
	if (chip_x_dim > 2*R_minus_m) or (chip_y_dim > 2*R_minus_m):
		vect_to_position = 'delete_flag'
	elif q1 or q2:
		if ((x_margin + chip_margin + chip_x_dim - R_minus_m)**2 + (R_minus_m - y_margin)**2) > 0:
			if (np.sqrt((x_margin + chip_margin + chip_x_dim - R_minus_m)**2 + (R_minus_m - y_margin)**2) > R_minus_m): # does not fit on current row (out of qI bounds)
				y_margin += (y_margin_winner + chip_margin)
				if y_margin < R_minus_m: # new row will still be in qII
					sqrt = np.sqrt(R_minus_m**2 - ((R_minus_m - y_margin)**2))
				elif (R_minus_m**2 - ((y_margin + chip_y_dim - R_minus_m)**2)) < 0: # new row will be in qIII but chip is too long in y to be within bounds of qIII
					(i, x_margin,y_margin,z_margin,y_margin_winner,z_margin_winner,new_layer_bool,vect_to_position) = new_layer(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, z_margin, chip_margin, y_margin_winner, z_margin_winner) # move to next layer
				else: # new row will be in qIII
					sqrt = np.sqrt(R_minus_m**2 - ((y_margin + chip_y_dim - R_minus_m)**2))
				if (chip_x_dim > 2*sqrt): # chip is too long in x to be within bounds
					(i, x_margin,y_margin,z_margin,y_margin_winner,z_margin_winner,new_layer_bool,vect_to_position) = new_layer(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, z_margin, chip_margin, y_margin_winner, z_margin_winner) # move to next layer
				else: # chip fits entirely on new row
					(x_margin, y_margin_winner, z_margin_winner, vect_to_position) = new_row(i,Vector, q2, R_minus_m, sqrt, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, z_margin_winner) # move to next row
			else:
				(x_margin, y_margin_winner, z_margin_winner, vect_to_position) = next_chip(i,Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner)
		else:
			vect_to_position = 'delete_flag'
	else:
		if ((x_margin + chip_margin + chip_x_dim - R_minus_m)**2 + (y_margin + chip_y_dim - R_minus_m)**2) > 0:
			if (np.sqrt((x_margin + chip_margin + chip_x_dim - R_minus_m)**2 + (y_margin + chip_y_dim - R_minus_m)**2) > R_minus_m): # does not fit on current row (out of qIV bounds)
				y_margin += (y_margin_winner + chip_margin)
				if y_margin + chip_y_dim > 2*R_minus_m: # would not fit anywhere on next row
					(i, x_margin,y_margin,z_margin,y_margin_winner,z_margin_winner,new_layer_bool,vect_to_position) = new_layer(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, z_margin, chip_margin, y_margin_winner, z_margin_winner) # move to next layer
				else:
					if (R_minus_m**2 - ((y_margin + chip_y_dim - R_minus_m)**2)) > 0:
						sqrt = np.sqrt(R_minus_m**2 - ((y_margin + chip_y_dim - R_minus_m)**2))
						(x_margin, y_margin_winner, z_margin_winner, vect_to_position) = new_row(i,Vector, q2, R_minus_m, sqrt, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, z_margin_winner) # move to next row
					else:
						vect_to_position = 'delete_flag'
			else:
				(x_margin, y_margin_winner, z_margin_winner, vect_to_position) = next_chip(i,Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner)
		else:
			vect_to_position = 'delete_flag'
	return (i, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner, new_layer_bool, vect_to_position)

def new_layer(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, z_margin, chip_margin, y_margin_winner, z_margin_winner):
	if (R_minus_m**2 - (chip_x_dim/2)**2) > 0:
		i = i*-1
		y_margin = R_minus_m - np.sqrt(R_minus_m**2 - (chip_x_dim/2)**2)
		x_margin = R_minus_m - (chip_x_dim/2)
		z_margin += z_margin_winner + chip_margin
		new_layer_bool = False
		vect_to_position = Vector([0,i*(R_minus_m - y_margin - (chip_y_dim/2)),z_margin+(chip_z_dim/2)])
		x_margin += chip_x_dim
		y_margin_winner = chip_y_dim
		z_margin_winner = chip_z_dim
	else:
		vect_to_position = 'delete_flag'
	return (i, x_margin,y_margin,z_margin,y_margin_winner,z_margin_winner,new_layer_bool,vect_to_position)

def new_row(i, Vector, q2, R_minus_m, sqrt, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, z_margin_winner):
	x_margin = R_minus_m - sqrt
	vect_to_position = Vector([i*(-R_minus_m + x_margin + (chip_x_dim)/2), i*(R_minus_m - y_margin - (chip_y_dim/2)),z_margin+(chip_z_dim/2)])
	x_margin += chip_x_dim + chip_margin
	y_margin_winner = chip_y_dim
	if chip_z_dim > z_margin_winner:
		z_margin_winner = chip_z_dim
	return (x_margin, y_margin_winner, z_margin_winner, vect_to_position)

def next_chip(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner):
	vect_to_position = Vector([i*(x_margin + chip_margin + (chip_x_dim/2) - R_minus_m), i*(R_minus_m - y_margin - (chip_y_dim/2)), z_margin+(chip_z_dim/2)])
	x_margin += chip_x_dim + chip_margin
	if chip_y_dim > y_margin_winner:
		y_margin_winner = chip_y_dim
	if chip_z_dim > z_margin_winner:
		z_margin_winner = chip_z_dim
	return (x_margin, y_margin_winner, z_margin_winner, vect_to_position)

def stack_subdivide(np,Vector,stack_number,original_jug_bounds,jug_thickness):
	# Subdivide a supertall stack according to its geometry
	# Access temporary scene and take relevant measurements of stack and jug
	scene = bpy.data.scenes[str(stack_number)] #+'_temp']
	jug_x_dim, jug_y_dim = float(original_jug_bounds['x_high'])- float(original_jug_bounds['x_low']), float(original_jug_bounds['y_high']) - float(original_jug_bounds['y_low'])
	jug_radius = 0.5*min(jug_x_dim, jug_y_dim)
	jug_edge_margin = 0.005
	R_minus_m = jug_radius - jug_edge_margin
	chip_margin = jug_edge_margin
	x_margin, y_margin, z_margin = 0, 0, 0 # guarantees first chip will fall in new layer
	y_margin_winner, z_margin_winner = 0, 0 # keep track of largest chip in each row (y) and layer (z)
	new_layer_bool = True # first chip placement initiates a new layer
	i = -1 # factor that determines whether the chips load clockwise or counterclockwise; alternates between +/- 1 after each new layer to ensure even distribution
	for item in scene.objects:
		if ("GH_Obj" in item.name) and ('_settled' not in item.name):
			# Measure chip dimensions
			chip_bounds = obj_bounds(bpy,Vector,item.name)
			x_max, y_max, z_max = float(chip_bounds['x_high']), float(chip_bounds['y_high']), float(chip_bounds['z_high'])
			x_min, y_min, z_min = float(chip_bounds['x_low']), float(chip_bounds['y_low']), float(chip_bounds['z_low'])
			chip_x_dim, chip_y_dim, chip_z_dim = x_max - x_min, y_max - y_min, z_max - z_min
			vect_to_origin = Vector([-item.location[0], -item.location[1], -item.location[2]])
			if new_layer_bool: # to catch first instance
				(i, x_margin,y_margin,z_margin,y_margin_winner,z_margin_winner,new_layer_bool,vect_to_position) = new_layer(i, Vector, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, z_margin, chip_margin, y_margin_winner, z_margin_winner)
			else:
				(q1, q2) = quad_test(R_minus_m,chip_x_dim,chip_y_dim,x_margin,y_margin,chip_margin)
				(i, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner, new_layer_bool, vect_to_position) = row_layer_filter(i, Vector, q1, q2, new_layer_bool, R_minus_m, chip_x_dim, chip_y_dim, chip_z_dim, chip_margin, x_margin, y_margin, z_margin, y_margin_winner, z_margin_winner)
			if vect_to_position != 'delete_flag':
				vect = vect_to_origin + vect_to_position
				translate(item,vect)
			else:
				delete_obj(item)

def manipulate_chip_stack(measurements_directory,chipStack_folder,chipStack_name,file,stack_number,realign_margin,original_jug_bounds,chip_thickness,Vector,jug_thickness,fill_height):
	active_scene = bpy.data.scenes[str(stack_number)]
	# Import chips and manipulate them
	import_chips_fbx(measurements_directory,chipStack_folder,chipStack_name,file,active_scene)
	import_chips_cleanup(chipStack_name)
	chipStack_bounds = stack_bounds(stack_number)
	stack_subdivide(np,Vector,stack_number,original_jug_bounds,jug_thickness)

def apply_physics(chip_thickness,stack_number):
	scene = bpy.data.scenes[str(stack_number)]
	for item in scene.objects:
		if ("GH_Obj" in item.name) and ('_settled' not in item.name):
			item.select = True
			bpy.context.scene.objects.active = item
			#	1. Remove chip_thickness modifier from chips that have already been imported to prevent double thickening
			try:
				bpy.ops.object.modifier_remove(modifier='Solidify')
				pass
			except Exception as e:
				raise e
				break
			#	Apply chip thickness
			bpy.ops.object.modifier_add(type='SOLIDIFY')
			bpy.context.object.modifiers['Solidify'].thickness = chip_thickness
			bpy.context.object.modifiers['Solidify'].offset = 0.0
			# 	2. Make chip stack rigid bodies and assign physics constants
			bpy.ops.rigidbody.object_add(type='ACTIVE')
			item.rigid_body.collision_shape = 'MESH'
			item.rigid_body.mesh_source = 'FINAL'
			item.rigid_body.linear_damping, item.rigid_body.angular_damping = 0.9, 0.9
			item.rigid_body.friction, item.rigid_body.restitution, item.rigid_body.collision_margin = 0.850, 0.200, 0.0 # <------ Let's think about this later.
			item.rigid_body.use_deactivation, item.rigid_body.use_start_deactivated = True, True
			#	3. Set chip color
			# item.data.materials[0].use_object_color = True
			# item.color = (0.800,0.435,0.028,1.000)
			item.select = False

def animate(stack_number):
	# Set scene animation constants
	scene = bpy.data.scenes[str(stack_number)]
	scene.rigidbody_world.time_scale = 0.75 # 0.35
	scene.rigidbody_world.steps_per_second = 500
	scene.rigidbody_world.solver_iterations = 30
	scene.rigidbody_world.point_cache.frame_end = 25 # 50
	# Bake (simulate) settlement and set frame to last
	bpy.ops.ptcache.bake_all(bake=True)
	bpy.context.scene.frame_set(scene.frame_end)
	# Apply transformation at last frame to coordinate matrices of object vertices
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.visual_transform_apply()
	bpy.ops.object.select_all(action='DESELECT')
	# Disable settled objects to prevent excessive jiggling
	for item in scene.objects:
		if ("GH_Obj" in item.name) and ('_settled' not in item.name):
			item.select = True
			bpy.context.scene.objects.active = item
			bpy.ops.rigidbody.object_add(type='PASSIVE')
		elif ("GH_Obj" in item.name) and ('_settled' in item.name):
			item.select = True
			bpy.context.scene.objects.active = item
			bpy.ops.rigidbody.object_add(type='ACTIVE')
			item.rigid_body.enabled = False
	bpy.ops.object.select_all(action='DESELECT')
	# Reset scene animation constants for ease of inspection upon script completion
	bpy.data.scenes[str(stack_number)].frame_start, bpy.data.scenes[str(stack_number)].frame_end = 2, scene.rigidbody_world.point_cache.frame_end

def settled_chips_rename(stack_number):
	scene = bpy.data.scenes[str(stack_number)]
	for item in scene.objects:
		if ("GH_Obj" in item.name) and ('_settled' not in item.name):
			item.name = item.name + '_settled_' + str(stack_number)

def obj_bounds(bpy,Vector,obj):
	# Find the dimenstions of the box bounding some object
	bound_obj = bpy.data.objects[obj]
	bbox_corners = [bound_obj.matrix_world * Vector(corner) for corner in bound_obj.bound_box]
	bbox_corners_tuples = [corner.to_tuple() for corner in bbox_corners]
	bounds = {'x_low':bbox_corners_tuples[0][0],'x_high':bbox_corners_tuples[6][0],
		'y_low':bbox_corners_tuples[0][1],'y_high':bbox_corners_tuples[6][1],
		'z_low':bbox_corners_tuples[0][2],'z_high':bbox_corners_tuples[6][2]}
	return bounds

def write_vertices_list(bpy,stack_number):
	# Write list of tuples of all chip vertices
	scene = bpy.data.scenes[str(stack_number)]
	chip_vertices_list = []
	for item in scene.objects:
		if ("GH_Obj" in item.name):
			verts = item.data.vertices
			verts_to_add = [item.matrix_world * vert.co for vert in verts]
			verts_to_add_tuples = [vert.to_tuple() for vert in verts_to_add]
			chip_vertices_list.extend(verts_to_add_tuples)
	return chip_vertices_list

def bag_fill(chip_vertices_list,original_jug_bounds,jug_thickness,null_flag):
	# For each bag or chip vertex, find the bucket it belongs to; if its z coordinate is higher than the current highest, it wins. If it is higher than the total highest, it wins
	stack_height = null_flag
	for vertex in chip_vertices_list:
		if (vertex[2] > stack_height):
			stack_height = vertex[2]
	fill_height = (stack_height - original_jug_bounds["z_low"]) # m
	return fill_height

def calc_bag_fill(stack_number,jug_thickness,original_jug_bounds):
	# Script to calculate fill height of chips in jug
	null_flag = -99999
	chip_vertices_list = write_vertices_list(bpy,stack_number)
	fill_height = bag_fill(chip_vertices_list,original_jug_bounds,jug_thickness,null_flag)
	return fill_height

def calc_vol_fill(fill_height):
	# Calculate volume (cm^3) fill from fill height
	H = 1482 + (1000*fill_height) # mm
	r = (float(80)/1482)*(1482+(1000*fill_height)) # mm
	vol_fill = ((3.1415926535/3)*((H*(r**2))-(9484800)))*(0.001) # cm^3
	return vol_fill

def calc_chip_mass(stack_number,density,chip_thickness):
	total_chip_mass = 0.0
	# Calculate the total mass (kg) of chips in scene
	scene = bpy.data.scenes[str(stack_number)]
	for item in scene.objects:
	    if ("GH_Obj" in item.name):
	    	item.select = True
	    	bpy.ops.rigidbody.mass_calculate(material='Custom', density=(density*(0.00053/chip_thickness))) # 0.00053 is actual weight-average chip_thickness
	    	total_chip_mass += item.rigid_body.mass
	    	item.select = False
	return total_chip_mass

def calc_bulk_density(total_chip_mass,vol_fill):
	bulk_density = (1000000*total_chip_mass)/(vol_fill)
	return bulk_density

def clean_scene(stack_number,original_jug_bounds,fill_height,jug_thickness):
	scene = bpy.data.scenes[str(stack_number)]
	bpy.ops.object.select_all(action='DESELECT')
	for item in scene.objects:
		if ("GH_Obj" in item.name):
			verts = item.data.vertices
			vertices = [item.matrix_world * vert.co for vert in verts]
			vertices_tuples = [vert.to_tuple() for vert in vertices]
			for vertex in vertices_tuples:
				r = ((float(80)/1482)*(1482+(1000*(vertex[2]-original_jug_bounds["z_low"]))))/1000
				if (np.sqrt(vertex[0]**2 + vertex[1]**2) > 1.05*r):
					item.select = True
					break
				elif (vertex[2] > 1.10*(original_jug_bounds['z_low']+fill_height)):
					item.select = True
					break
				elif (vertex[2] < 1.0*original_jug_bounds['z_low']):
					item.select = True
					break
	bpy.ops.object.delete()

def output_data_org(file,output_data,data_dicts):
	# Write dictionaries including relevant output information
	data_dict = {'file': file, 'total_chip_mass': output_data[0], 'fill_height': output_data[1], 'vol_fill': output_data[2], 'bulk_density': output_data[3]}
	data_dicts.append(data_dict)
	return data_dicts

def csv_writer(csv,os,data_dicts,measurement_folder):
	directory = "G:\"+ measurement_folder
	if not os.path.exists(directory):
		os.makedirs(directory)
	with open(directory + '/' + 'outputs.csv', 'w', newline='') as csvfile:
		# Write output information in dictionaries
		fieldnames = ['File', 'Chip mass (kg)', 'Fill height (m)', 'Fill volume (cm^3)', 'Bulk density (g/L)']
		writer = csv.DictWriter(csvfile,fieldnames)
		writer.writeheader()
		# Set counters to find averages of output data for ease of comparison against other stack typologies
		average_mass, average_height, average_fill, average_density = 0, 0, 0, 0
		for data in data_dicts:
			writer.writerow({'File': data['file'], 'Chip mass (kg)': data['total_chip_mass'], 'Fill height (m)': data['fill_height'], 'Fill volume (cm^3)': data['vol_fill'], 'Bulk density (g/L)': data['bulk_density']})
			average_mass += data['total_chip_mass']
			average_height += data['fill_height']
			average_fill += data['vol_fill']
			average_density += data['bulk_density']
		average_mass, average_height, average_fill, average_density = average_mass/len(data_dicts), average_height/len(data_dicts), average_fill/len(data_dicts), average_density/len(data_dicts)
		writer.writerow({'File': 'AVERAGES', 'Chip mass (kg)': average_mass, 'Fill height (m)': average_height, 'Fill volume (cm^3)': average_fill, 'Bulk density (g/L)': average_density})

def export_scene(os,measurement_folder,chipStack_folder):
	# Export final geometry as FBX
	directory = "G:\"+ measurement_folder
	if not os.path.exists(directory):
		os.makedirs(directory)
	bpy.ops.export_scene.fbx(filepath = directory + '/' + chipStack_folder + '.fbx')

main()
