#!/home/xubinghui/anaconda3/bin/python

# ==============================================================================
# -- find carla module and import ---------------------------------------------------------
# ==============================================================================
'''#!/usr/bin/env python'''


import glob
import os
import sys
import time
import random
import numpy as np
import cv2
'''
# useless in carla 0.9.14
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
'''
import carla

IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image):
    i = np.array(image.raw_data)  # long vector not matrix
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))  # 4--R,G,B,Alpha
    i3 = i2[:, :, :3]  # don't need alpha
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0  # normalization data to 0~1

actor_list=[]
try:
    # ==============================================================================
    # connect carla client
    # ==============================================================================


    client=carla.Client("localhost",2000)
    client.set_timeout(2.0)

    # ==============================================================================
    # set the world
    # ==============================================================================
    
    # ===import a new world
    # world=client.load_world("/home/xubinghui/carla/HDMaps/Town05.pcd")
    # ===otherwise use the present world
    world=client.get_world()

    # ==============================================================================
    # generate the actor
    # ==============================================================================

    blueprint_library=world.get_blueprint_library()
    my_vehicle_bp=blueprint_library.filter("model3")[0]
    print()
    '''
    blueprints in https://carla.readthedocs.io/en/latest/bp_library/
    '''
    my_vehicle_bp.set_attribute("color","0,0,0")

    # ==============================================================================
    # transform the car position and spwan the car
    # ==============================================================================
    # fix point mode ========================
    # location=carla.Location(0,10,0)
    # rotation=carla.Rotation(0,0,0)
    # transform_vehicle=carla.Transform(location,rotation)
    
    # random mode =============================
    # transform means the point to generate the car
    transform_vehicle = random.choice(world.get_map().get_spawn_points())

    my_vehicle=world.spawn_actor(my_vehicle_bp,transform_vehicle)
    actor_list.append(my_vehicle)

    # ==============================================================================
    # set control mode
    # ==============================================================================
    
    # auto pilot mode========
    # my_vehicle.set_autopilot(enabled=True)
    # time.sleep(1) 
    # world.tick()
    
    # manual mode=======
    my_vehicle.apply_control(carla.VehicleControl(throttle=1.0,steer=0.0))#speed=full,change direction=0
    
    # ==============================================================================
    # set camera
    # ==============================================================================
    my_camera_bp=blueprint_library.find("sensor.camera.rgb")



    my_camera_bp.set_attribute("image_size_x","{}".format(IM_WIDTH))
    my_camera_bp.set_attribute("image_size_y","{}".format(IM_HEIGHT))
    my_camera_bp.set_attribute("fov","110")
    # ==============================================================================
    # set camera location and fix it on the car
    # ==============================================================================
    transform_camera=carla.Transform(carla.Location(x=2.5,z=0.7))
    my_camera=world.spawn_actor(my_camera_bp,transform_camera,attach_to=my_vehicle)
    actor_list.append(my_camera)
    # ==============================================================================
    # listen to camera data with window
    # ==============================================================================
 
    my_camera.listen(lambda data: process_img(data))
    # time.sleep(0.01)
    # world.tick()
    
    time.sleep(10)
    

    
    

    # ==============================================================================
    # listen to camera data
    # ==============================================================================
    
    # while True:
        # spectator=world.get_spectator()
        # transform_s=my_vehicle.get_transform()
        # spectator.set_transform(carla.Transform(transform_s.location+carla.Location(x=2.5, z=1.2),carla.Rotation()))
        # time.sleep(0.01)
# except:
#     pass
    
    
    
finally:
    for actor in actor_list:
        actor.destroy()
    print("cleaned generated actors")