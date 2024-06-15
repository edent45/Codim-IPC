import sys
sys.path.insert(0, "../../Python")
import Drivers
from JGSL import *

if __name__ == "__main__":
    sim = Drivers.FEMDiscreteShellBase("double", 3)

    size = 10
    N = 10

    sim.mu = 0.4

    #simulation parameters:
    #density - how tightly a material is packed together 
    density = 8.96
    #elastic modulus - the stiffness of a material - how easily it is bended or stretched
    young_modulus = sim.cloth_Ebase[0]
    #the ratio of transverse contraction strain to longitudinal extension strain in the direction of the stretching force
    poisson_ratio = 0.3 #rubber is 0.4999 , steel is 0.3 , wire whose volume remains - 0.5 , 
    thickness = sim.cloth_thickness[1]


    #setup
    # Add a 3d model that represents Floor (Bottom Plane)
    sim.add_shell_3D("input/square21.obj", Vector3d(0, -0.16, 0), \
        Vector3d(0, 0, 0), Vector3d(0, 1, 0), 0)
    sim.set_DBC(Vector3d(-0.1, -0.1, -0.1), Vector3d(1.1, 1e-3, 1.1), 
        Vector3d(0, 0, 0), Vector3d(0, 0, 0), Vector3d(0, 1, 0), 0)
    # Set the Dirichlet Boundary Condition (floor remains stationary)
 
    
    
    # rod:
    step = 0.08 / (N - 1)
    for i in range(N):
        for j in range(N):
            sim.make_and_add_rod_3D(0.6, int(size), Vector3d(-0.04 + step * i, 0.2, -0.04 + step * j), \
                Vector3d(0, 0, 0), Vector3d(0, 0, 1), 90, Vector3d(1, 1, 1)) # can add some random tilt



    #simulation parameters:
    sim.dt=0.02 #time step
    sim.frame_dt = 0.02 #fram rate
    sim.frame_num = 100 #number of frames
    sim.withCollision = True
    sim.epsv2 = 1e-10

      #initialize 
    sim.initialize(density, sim.cloth_Ebase[0], 0.4, \
            sim.cloth_thickness[1], 0)
  
    sim.initialize_rod(160, 1e3, 1, 1.5e-3)
    
    sim.initialize_OIPC(5e-4, 1e-3) # can change offset
    

    sim.run()


