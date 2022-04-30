import bpy
import math

class camera():
    def __init__(self) -> None:
        pass
    

    def look_at(obj_camera, point):
        loc_camera = obj_camera.location

        direction = mathutils.Vector(point) - loc_camera
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')

        # assume we're using euler rotation
        obj_camera.rotation_euler = rot_quat.to_euler()


    def update_camera_pos(cam_target, cam_radius):
        #Update camera position
        cam = bpy.data.objects['Camera']
        t_loc_x = cam_target['x']
        t_loc_y = cam_target['y']

        alpha = random.random()*math.tau
        cam.location.x = t_loc_x+math.cos(alpha) * cam_radius
        cam.location.y = t_loc_y+math.sin(alpha) * cam_radius
        cam.location.z = 1

        look_at(cam, cam_target.values())