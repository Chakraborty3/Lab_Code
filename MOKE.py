from srsinst.sr860 import SR860

# only required for USB or GPIB communication
import pyvisa as visa 
lockin = SR860('vxi11', '192.168.0.4')
import time
import numpy as np
import matplotlib.pyplot as plt

lockin.signal.time_constant = 1.0     # seconds


lockin.signal.filter_slope = 18       # dB/oct
lockin.signal.advanced_filter = 'off' # or 'on'

# Wait ~5×tau for ~99% settling (SR860 manual guidance)
wait_time_s = lockin.signal.time_constant
print(f"Time/measurement = {wait_time_s} s")


num_points = 10                       # set 100 for a longer sweep
offset = np.linspace(-1.0, 1.0, num=num_points)  # example: sweep -1 V to +1 V

X, Y, R, Theta = [], [], [], []
t_elapsed = []

# Start with initial DC offset; give one full settle
lockin.ref.sine_out_offset = float(offset[0])
time.sleep(wait_time_s)

t0 = time.monotonic()

for vdc in offset:
    lockin.ref.sine_out_offset = float(vdc)
    time.sleep(wait_time_s)  # allow lock-in to settle

    # Read channels (X, Y, R, Theta)
    x, y, r, theta = lockin.data.get_channel_values()
    X.append(x); Y.append(y); R.append(r); Theta.append(theta)

    # Real elapsed time from start (seconds)
    t_elapsed.append(time.monotonic() - t0)

R_uV = np.array(R) * 1e6
plt.figure()
plt.plot(t_elapsed, R_uV, marker='o', label='R (µV)')
plt.xlabel('Time (s)')
plt.ylabel('R (µV)')
plt.title('Measured R vs Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()