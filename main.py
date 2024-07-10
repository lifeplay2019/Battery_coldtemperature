import pybamm
import numpy as np
import matplotlib.pyplot as plt

# Set up model and parameters
options = {"thermal": "lumped"}
DFN_18650 = pybamm.lithium_ion.DFN(options=options)
param = DFN_18650.param
parameters = pybamm.ParameterValues("Mohtat2020")
parameters["Initial concentration in positive electrode [mol.m-3]"] = 38000.0

# Calculate stoichiometries at 100% SOC
x_0, x_100, y_100, y_0 = pybamm.lithium_ion.get_min_max_stoichiometries(
    parameters, param
)

# Update parameter values with initial conditions
c_n_max = parameters["Maximum concentration in negative electrode [mol.m-3]"]
c_p_max = parameters["Maximum concentration in positive electrode [mol.m-3]"]
parameters.update(
    {
        "Initial concentration in negative electrode [mol.m-3]": x_100 * c_n_max,
        "Initial concentration in positive electrode [mol.m-3]": y_100 * c_p_max,
    }
)

# Experiment setup
experiment = pybamm.Experiment(
    [
        "Discharge at 1C for 60 minutes (1 second period)",
        "Rest for 10 minutes (1 second period)",
    ]
    * 10
)

# Solving the model
var_pts = {"x_n": 30, "x_s": 30, "x_p": 30, "r_n": 10, "r_p": 10}
pybamm.set_logging_level("NOTICE")
sim_DFN = pybamm.Simulation(
                            DFN_18650,
                            experiment=experiment,
                            parameter_values=parameters,
                            var_pts=var_pts
)
sim_DFN.solve()

# Outputs
solution_DFN = sim_DFN.solution
t_DFN = solution_DFN["Time [s]"].entries

x = solution_DFN["Average negative particle concentration"].entries
cell_SoC_x = 100 * (x - x_0) / (x_100 - x_0)

y = solution_DFN["Average positive particle concentration"].entries
cell_SoC_y = 100 * (y - y_0) / (y_100 - y_0)

Total_heating_DFN = solution_DFN["Total heating [W.m-3]"].entries
Ohmic_heating_DFN = solution_DFN["Ohmic heating [W.m-3]"].entries
Cell_Temp_DFN = solution_DFN["Cell temperature [K]"].entries

print("SoC from x and y should match:", np.allclose(cell_SoC_x, cell_SoC_y))

# Plots
fig, axs = plt.subplots(1, 2)

axs[0].plot(t_DFN, cell_SoC_x)
axs[0].set_title("Negative SOC as a function of time")
axs[0].set(xlabel="Time [in s]")
axs[0].set(ylabel="Negative SOC [in %]")

axs[1].plot(t_DFN, cell_SoC_y)
axs[1].set_title("Positive SOC as a function of time")
axs[1].set(xlabel="Time [in s]")
axs[1].set(ylabel="Positive SOC [in %]")

Cell_volume = parameters["Cell volume [m3]"]
Total_heating_DFN = np.average(Total_heating_DFN, axis=0) * Cell_volume
Ohmic_heating_DFN = np.average(Ohmic_heating_DFN, axis=0) * Cell_volume
Cell_Temp_DFN = np.average(Cell_Temp_DFN, axis=0)

fig, axs = plt.subplots(1, 3)
axs[0].plot(t_DFN, Total_heating_DFN)
axs[0].set_title("Total heating as a function of time")
axs[0].set(xlabel="Time [in s]")
axs[0].set(ylabel="Total heating [W]")

axs[1].plot(t_DFN, Ohmic_heating_DFN)
axs[1].set_title("Joule heating as a function of time")
axs[1].set(xlabel="Time [in s]")
axs[1].set(ylabel="Joule heating [W]")

axs[2].plot(t_DFN, Cell_Temp_DFN)
axs[2].set_title("Average cell temperature as a function of time")
axs[2].set(xlabel="Time [in s]")
axs[2].set(ylabel="Cell temperature [K]")
plt.show()