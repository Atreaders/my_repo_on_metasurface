import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_openscad_script(filename="silicon_pillars.scad"):
    # Parameters
    pillar_diameter = 5  # microns
    pillar_radius = pillar_diameter / 2
    pillar_height = 1  # microns
    num_pillars = 100
    grid_size = int(np.sqrt(num_pillars))
    spacing = 10  # microns
    substrate_thickness = 10  # microns
    substrate_size = 105  # microns (square 105x105)
    
    with open(filename, "w") as f:
        # Create SiO2 Substrate
        f.write(f"cube([{substrate_size}, {substrate_size}, {substrate_thickness}]);\n")
        
        # Create the Si pillars in a grid
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * spacing + spacing / 2
                y = j * spacing + spacing / 2
                f.write(f"translate([{x}, {y}, {substrate_thickness}]) cylinder(h={pillar_height}, r={pillar_radius}, center=false);\n")
    
    print(f"OpenSCAD script saved as {filename}")

def plot_pillars():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Define substrate
    substrate_x = [0, 0, 105, 105]
    substrate_y = [0, 105, 105, 0]
    substrate_z = [0, 0, 0, 0]
    verts = [list(zip(substrate_x, substrate_y, substrate_z))]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.3, facecolor='gray'))
    
    # Create pillars
    grid_size = int(np.sqrt(100))
    spacing = 10
    for i in range(grid_size):
        for j in range(grid_size):
            x = i * spacing + spacing / 2
            y = j * spacing + spacing / 2
            ax.bar3d(x, y, 10, 5, 5, 1, shade=True, color='red')
    
    ax.set_xlim([0, 105])
    ax.set_ylim([0, 105])
    ax.set_zlim([0, 12])
    ax.set_xlabel("X (microns)")
    ax.set_ylabel("Y (microns)")
    ax.set_zlabel("Height (microns)")
    ax.set_title("3D Visualization of Silicon Pillars on SiO2 Substrate")
    
    plt.show()

generate_openscad_script()
plot_pillars()
