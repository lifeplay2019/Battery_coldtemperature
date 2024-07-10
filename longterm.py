import pybamm
import pandas as pd
import os

os.chdir(pybamm.__path__[0] + "/..")

pybamm.set_logging_level("INFO")

# load model and update parameters so the input current is the US06 drive cycle
model = pybamm.lithium_ion.SPMe({"thermal": "lumped"})
param = model.default_parameter_values


# import drive cycle from file
drive_cycle = pd.read_csv(
    "pybamm/input/drive_cycles/US06.csv", comment="#", header=None
).to_numpy()

# create interpolant
timescale = param.evaluate(model.timescale)
# in the following line we use % 600 to repeat the drive cycle every 600 seconds
current_interpolant = pybamm.Interpolant(drive_cycle, (timescale * pybamm.t) % 600)

# set drive cycle
param["Current function [A]"] = current_interpolant


# create and run simulation using the CasadiSolver in "fast" mode, remembering to
# pass in the updated parameters
sim = pybamm.Simulation(
    model, parameter_values=param, solver=pybamm.CasadiSolver(mode="fast")
)
# we need to specify the solve time to be different from the default [0, 600]
# this will raise a warning but this can be ignored
sim.solve([0, 1800])
# use this instead to get rid of the warning
# t_drive = drive_cycle[:, 0]
# step_size = np.min(np.diff(t_drive))
# t_eval = np.arange(0, 1800, step_size)
# sim.solve(t_eval)
# you can play with step_size to change the level of resolution of the drive cycle

sim.plot(
    [
        "Negative particle surface concentration [mol.m-3]",
        "Electrolyte concentration [mol.m-3]",
        "Positive particle surface concentration [mol.m-3]",
        "Current [A]",
        "Negative electrode potential [V]",
        "Electrolyte potential [V]",
        "Positive electrode potential [V]",
        "Terminal voltage [V]",
        "X-averaged cell temperature",
    ]
)