import bpy
import mathutils
import os
import glob
import json
import sys
import random

import time



dir = os.path.dirname(__file__)
if not dir in sys.path:
   sys.path.append(dir)
from blend_vision import scene, data, render_utils

data_dir = './data'
dataset_name = 'ShapeNetCore.v2'
json_name = 'shapenetcore.taxonomy.json'
model_name = 'model_normalized.obj'
target_classes = ['camera']

scene_obj = scene() # scene(engine='CYCLES', device='GPU)
scene_data = data()
scene_render = render_utils.render()


scene_data.load_obj_paths()
scene_data.render_path()
scene_obj.clean_up()


for class_path in scene_data.class_paths:
    
    model_files = glob.glob(os.path.join(data_dir, dataset_name, class_path, '**', '*.obj'), recursive=True)
    for i, model_file in enumerate(model_files):
        
        SEED = time.time()
        random.seed(SEED)

        # Parse path
        model_file_split = model_file.split('/')
        model_hash_index = -2
        if model_file_split[-2] == 'models':
            model_hash_index = -3

        # Import
        bpy.ops.import_scene.obj(filepath=model_file)
        
        # Are these lines needed?
        obj = bpy.context.selected_objects[0]
        
        rand_gen = random.Random()
        obj.location = (rand_gen.uniform(-2, 2), rand_gen.uniform(-2, 2),rand_gen.uniform(-2, 2))
        
        
        collection_name = model_file_split[model_hash_index]
        obj_name = model_file_split[-1].replace('.obj', '')
        
        
        # Init collection
        myCol = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(myCol)
        # Check if mesh is in collection
        check_collection = [i for i in bpy.context.scene.collection.objects]
        # add mesh to correct collection
        for o in bpy.context.selected_objects:
            myCol.objects.link(o)
            
            if check_collection:
                bpy.context.scene.collection.objects.unlink(o)
        
        if i > 0:
            break

    # Render label pass
    bpy.context.scene.render.filepath = os.path.join(data_dir, 'Labels', model_file_split[model_hash_index])
    scene_render.label_objs(bpy.data.objects)
    bpy.ops.render.render(write_still = True)
    scene_render.segmentation_reset(objs=bpy.data.objects, scene=scene_obj)
    
    # Render final pass
    scene_render.composition_setup()
    bpy.context.scene.render.filepath = os.path.join(data_dir, 'Renders', model_file_split[model_hash_index])
    bpy.ops.render.render(write_still = True)
    scene_render.composition_reset()

        # Remove Collection
        # bpy.data.collections.remove(myCol)

        # scene_obj.clean_up()

