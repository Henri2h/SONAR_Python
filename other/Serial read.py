import serial
import matplotlib.pyplot as plt

print("Hello, starting ...")

if (True):
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/ttyACM0'
    ser.open()
    ser.write(b'start\n')
    
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())

    print("===========")
    print("Done : ")
    print("===========")
    i = 0
    cond = True
    X = []
    Y = []
    t0 = 0
    for r in range(1):
        ser.write(b'get\n')
        
        dt = int(ser.readline())/1000000

        cond = True
        while(cond):
            
            text = ser.readline()
            
            inputs = str(text.decode()).strip()
        
            a = inputs.split(";")
            time = float(a[0])/14000*dt
            
            data = float(a[1])
            X.append(time)
            Y.append(data)
            print(str(i) + " : " + a[0] + " t:" + str(time) +  " " + str(data))
            
            i += 1

            if(i > 14000):
                cond = False
        print(dt)

    plt.plot(X,Y)
    plt.ylim([0,1024])
    plt.show()

