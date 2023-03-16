#!/usr/bin/env python

# ==============================================================================
# -- find carla module and import ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys
import time
import random
import numpy as np
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

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
    my_vehicle_bp=blueprint_library.find("vehicle.audi.a2")
    '''
    blueprints in https://carla.readthedocs.io/en/latest/bp_library/
    '''
    my_vehicle_bp.set_attribute("color","0,0,0")

    # ==============================================================================
    # transform the car position and spwan the car
    # ==============================================================================
    # fix point mode ====================
    # location=carla.Location(0,10,0)
    # rotation=carla.Rotation(0,0,0)
    # transform_vehicle=carla.Transform(location,rotation)
    # random mode =============================
    transform_vehicle = random.choice(world.get_map().get_spawn_points())

    my_vehicle=world.spawn_actor(my_vehicle_bp,transform_vehicle)

    # ==============================================================================
    # set control mode
    # ==============================================================================
    print(type(my_vehicle))
    # auto pilot mode
    my_vehicle.set_autopilot(enabled=True)
    time.sleep(1) 
    world.tick()
    # otherwise use the present model'''
    # my_vehicle.apply_control(carla.VehicleControl(throttle=1.0,steer=0.0))
    
    # ==============================================================================
    # set camera
    # ==============================================================================
    my_camera_bp=blueprint_library.find("sensor.camera.rgb")

    IM_WIDTH = 640
    IM_HEIIGHT = 480

    my_camera_bp.set_attribute("image_size_x","{}".format(IM_WIDTH))
    my_camera_bp.set_attribute("image_size_y","{}".format(IM_HEIIGHT))
    my_camera_bp.set_attribute("fov","90")
    # ==============================================================================
    # set camera location and fix it on the car
    # ==============================================================================
    transform_camera=carla.Transform(carla.Location(x=2.4,z=0.5))
    my_camera=world.spawn_actor(my_camera_bp,transform_camera,attach_to=my_vehicle)
    
    # ==============================================================================
    # listen to camera data with window
    # ==============================================================================
    '''
    my_camera.listen(lambda data: process_img(data))
    
    def process_img(image):
        i=np.array(image.raw_data)
        i2=i.reshape((640,480,4))
        i3=i2[:,:,:3]
        cv2.imshow("", i3)
        cv2.waitKey(1)
        return i3/255.0
    '''
    # ==============================================================================
    # listen to camera data
    # ==============================================================================
    
    while True:
        spectator=world.get_spectator()
        transform_s=my_vehicle.get_transform()
        spectator.set_transform(carla.Transform(transform_s.location+carla.Location(x=2.5, z=1.2),carla.Rotation()))
        time.sleep(0.01)
except:
    pass
    
    
    
# finally:
#     for actor in actor_list:
#         actor.destroy()
#     print("cleaned generated cars")