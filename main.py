import genesis as gs
import time
import numpy as np
from scipy.spatial.transform import Rotation as R



# =========================
# Scene setup
# =========================
gs.init()
scene = gs.Scene(show_viewer=True)
#scene.add_entity(gs.morphs.Plane())

# Add the drone
drone = scene.add_entity(
    gs.morphs.Drone(
        file="assets/robots/draugas/draugas_genesis.urdf",
        pos=(-3, -5, 8),  # start 5 meter above ground
        euler=(0, 0, 90),
    )
)


vineyard = scene.add_entity(
    gs.morphs.Mesh(
        file="assets/scene/vineyard-eltville-germany/source/vineyard_fixed_normals.obj",
        file_meshes_are_zup=True, 
        fixed=True,
        euler=(90, 0, 0),
        decimate=False,
        scale=2.0,
        ))



# =========================
# Add Drone Camera 
# =========================

cam = scene.add_camera(GUI=True, fov=70, )

# Using 'zyx' sequence: Yaw, Pitch, Roll
rotation = R.from_euler('zyx', [-90, -90, 0], degrees=True)

T = np.eye(4)
T[:3, :3] = rotation.as_matrix()

T[2, 3] = -0.1

cam.attach(drone.get_link("base"), T)


# =========================
# Build Scene
# =========================

scene.build()



target_height = 6.0
kp = 5000.0


for _ in range(1500):

    pos = drone.get_pos()  # Get the full tensor
    #print(pos)
    error = target_height - pos[2].item()

    base_rpm = 1475.8
    correction = kp * error
    rpms = np.clip([base_rpm + correction] * 4, 0, 25000)

    drone.set_propellels_rpm(rpms)
    scene.step()
    cam.move_to_attach()
    cam.render(depth=True)





