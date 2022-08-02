import LabosaTrack as lst
import orbit_prediction as op
import serial, sys

my_lat=-34.54
my_lon=-58.5
sat_name="ISS (ZARYA)"
time_delta=1 #seconds
elevation_start=10 #degrees
mechanical_resolution=0.9/16
mode = 1

try:
    serial_device=serial.Serial(port='COM8', baudrate=9600,stopbits=1,timeout=1,write_timeout=1)
except:
    print("ERROR: Couldn't connect to serial port")
    sys.exit()

if(mode==0):
    #### 0 Calculate ISS pass 
    orbit = lst.SatTrack(my_lat, my_lon, sat_name, time_delta, elevation_start)
    steps,start_data = lst.Orbit2steps(orbit, mechanical_resolution)
    compressed_steps = lst.CompressOrbitData(steps)
    
    lst.SerialSend(serial_device,compressed_steps,start_data)

if(mode==1):
    ### 1 Calculate next sat pass
    TLEs = op.DownloadTLEs()
    sat = op.NextSatPass(TLEs,my_lat,my_lon,7,40)
    print(sat.name)
    orbit = lst.SatTrack(my_lat, my_lon, sat.name, time_delta, elevation_start)
    steps,start_data = lst.Orbit2steps(orbit, mechanical_resolution)
    compressed_steps = lst.CompressOrbitData(steps)
    
    lst.SerialSend(serial_device,compressed_steps,start_data)