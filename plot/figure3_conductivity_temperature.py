import pybamm
import matplotlib.pyplot as plt


temperatures = [10, 25, 40]
def plot_capacity_and_conductivity(temperatures):
    model = pybamm.lithium_ion.SPMe()

    for temp in temperatures:
        param = model.default_parameter_values
        param.update({'Ambient temperature [K]': temp + 273.15})

        sim = pybamm.Simulation(model, parameter_values=param)
        sim.solve([0, 3600])

        try:
            # Update variable name here
            capacity = sim.solution['X-averaged positive dead lithium concentration [mol.m-3]']
            conductivity = sim.solution["Electrolyte conductivity [S.m-1]"]

            plt.figure(1)
            plt.plot(sim.solution.t, capacity.entries, label=f'{temp}°C')

            plt.figure(2)
            plt.plot(sim.solution.t, conductivity.entries, label=f'{temp}°C')
        except KeyError as e:
            print(f"Variable error: {e}")

    plt.figure(1)
    plt.title("Relative Capacity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Relative Capacity")
    plt.legend()
    plt.grid(True)

    plt.figure(2)
    plt.title("Ionic Conductivity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Ionic Conductivity [S.m-1]")
    plt.legend()
    plt.grid(True)

    plt.show()


plot_capacity_and_conductivity(temperatures)