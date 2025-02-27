import tidy3d as td
import numpy as np
import matplotlib.pyplot as plt

# Define constants
um = 1e-6  # Micron conversion
wavelength = 1.55 * um  # 1550 nm in microns

# Define materials
Si = td.Medium(permittivity=3.45**2)  # Silicon
SiO2 = td.Medium(permittivity=1.44**2)  # Silica (SiO2)

# Define geometry
substrate = td.Structure(
    geometry=td.Box(center=(0, 0, -1.5 * um), size=(td.inf, td.inf, 3 * um)),
    medium=SiO2,
)

mmi_region = td.Structure(
    geometry=td.Box(center=(0, 0, 0.25 * um), size=(td.inf, 0.5 * um, 0.5 * um)),
    medium=Si,
)

# Define simulation domain
sim_size = (4 * um, 2 * um, 4 * um)  # (x, y, z)

# Define source (TE-polarized waveguide mode source)
source = td.ModeSource(
    center=(-1.5 * um, 0, 0.25 * um),
    size=(0, 0.4 * um, 0.5 * um),
    source_time=td.GaussianPulse(freq0=td.C_0 / wavelength, fwidth=td.C_0 / (10 * wavelength)),
    direction="+",
    mode_spec=td.ModeSpec(num_modes=1, target_neff=3.45),
)

# Define field monitors
monitor_xy = td.FieldMonitor(  # XY Plane Monitor (Top-down View)
    center=(1.5 * um, 0, 0.25 * um),
    size=(0, 1 * um, 0.5 * um),
    freqs=[td.C_0 / wavelength],
    name="field_xy",
)

monitor_yz = td.FieldMonitor(  # YZ Plane Monitor (Side View)
    center=(0, 0, 0.25 * um),
    size=(4 * um, 2 * um, 0),
    freqs=[td.C_0 / wavelength],
    name="field_yz",
)

monitor_zx = td.FieldMonitor(  # ZX Plane Monitor (Cross-sectional View)
    center=(0, 0, 0),
    size=(4 * um, 0, 4 * um),
    freqs=[td.C_0 / wavelength],
    name="field_zx",
)

# Define simulation setup
sim = td.Simulation(
    size=sim_size,
    grid_spec=td.GridSpec.uniform(dl=0.1 * um),
    structures=[substrate, mmi_region],
    sources=[source],
    monitors=[monitor_xy, monitor_yz, monitor_zx],
    run_time=1e-17,  # 1 picosecond
    boundary_spec=td.BoundarySpec(
        x=td.Boundary.periodic(),
        y=td.Boundary.periodic(),
        z=td.Boundary.pml()
    ),
)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sim.plot_eps(z=0.25 * um, ax=axes[0])
axes[0].set_title("Permittivity (XY Plane)")

sim.plot_eps(y=0, ax=axes[1])
axes[1].set_title("Permittivity (XZ Plane)")

sim.plot_eps(x=0, ax=axes[2])
axes[2].set_title("Permittivity (YZ Plane)")

plt.show()
# Run simulation
fig, ax = plt.subplots(figsize=(4, 2))
sim.plot(z=0.25 * um, ax=ax)
plt.show()

# job = td.web.Job(simulation=sim, task_name="mmi_splitter", verbose=True)
# sim_data = job.run(path="mmi_splitter_data.hdf5")

# # Plot field results for different planes
# sim_data.plot_field("field_xy", "Ey", val="real")
# plt.title("Field Distribution (XY Plane)")
# plt.show()

# sim_data.plot_field("field_yz", "Ey", val="real")
# plt.title("Field Distribution (YZ Plane)")
# plt.show()

# sim_data.plot_field("field_zx", "Ey", val="real")
# plt.title("Field Distribution (ZX Plane)")
# plt.show()
