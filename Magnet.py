from qcodes.instrument_drivers.cryomagnetics import CryomagneticsModel4G
max_current_limits = {
    1: (40.0, 0.6944),
    2: (78, 0.3842),
    
}
coil_constant = 0.06478  # T/A

cryo_instrument = CryomagneticsModel4G(
    name="cryo_4g",
    address="GPIB::1::INSTR",
    max_current_limits=max_current_limits,
    coil_constant=coil_constant,
    pyvisa_sim_file="cryo4g.yaml",
)
# Checking the coil constant
coil_constant = cryo_instrument.coil_constant
print(f"Coil constant = {coil_constant} T/A")

import time

import matplotlib.pyplot as plt


# Function to plot magnetic field over time
def plot_field_over_time(cryo_instr, target, duration):
    times = []
    fields = []
    start_time = time.time()
    while (time.time() - start_time) < duration:
        fields.append(cryo_instr.field())
        times.append(time.time() - start_time)
        time.sleep(0.5)
    plt.plot(times, fields, marker="o")
    plt.xlabel("Time (s)")
    plt.ylabel("Magnetic Field (T)")
    plt.title(f"Time vs Magnetic Field towards {target} T")
    plt.show()
