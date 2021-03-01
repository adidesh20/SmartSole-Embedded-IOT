from manometer import *
bus = smbus2.SMBus(1)

sensor = PressureSensor (bus)
walk_threshold=16
walk_count=0
while True:
    total=0
    mode=-1
    walk_total=0     
    for y in range (100):
                
        for x in range(30):
            v=sensor.read()
            if v>mode:
                mode=v
            if v>walk_threshold:
                walk_total+=v
                walk_count+=1

            total+=v
            time.sleep(0.1)
        avg= total/30
        walk_avg= walk_total/walk_count
        ## send mode,avg and walk_avg to server now
    long_avg=total/3000
    ## send long_vg to server 
    
