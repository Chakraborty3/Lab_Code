from srsinst.sr860 import SR860

# only required for USB or GPIB communication
import pyvisa as visa 
lockin = SR860('vxi11', '192.168.0.4')
