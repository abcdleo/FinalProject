THRESHOLD = (120, 165)
THRESHOLD_COLOR = (60, 70, -25, -10, -20, -5)

BINARY_VISIBLE = False

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
    return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
count = 0
task = 1

while(True):
    clock.tick()
    img = sensor.snapshot()
    #img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()
    # img = sensor.snapshot().binary([THRESHOLD_COLOR]) if BINARY_VISIBLE else sensor.snapshot()

    #line = img.get_regression([(255, 255) if BINARY_VISIBLE else THRESHOLD], False, (0, 0 , 160, 25))
    line = img.get_regression([(255, 255) if BINARY_VISIBLE else THRESHOLD_COLOR], False, (0, 0 , 160, 25))

    find = False
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        #print("id = %d" %tag.id())
        find = True
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        # The conversion is nearly 6.2cm to 1 -> translation
        #print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
           #degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        # Translation units are unknown. Rotation units are in degrees.
        #print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
        #uart.write(("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args).encode())
        dist = math.sqrt(pow(tag.y_translation(), 2) + pow(tag.z_translation(), 2)) * 2.52
        #print("dist = %f" %(dist))
        off_axis = tag.cx()- 72
        #print ("cx = %f, c_y = %f, off_axis = %f" %(tag.cx(), tag.cy(), off_axis))
        if (tag.id() == 2):
            if (degrees(tag.y_rotation()) > 10 and degrees(tag.y_rotation()) < 180) :
                count = 0
                if (abs(off_axis) < 15) :
                    print ("turn right1")
                    uart.write (("/turn/run -50 \r\n").encode())
                elif (off_axis < -50) :
                    print ("turn right7")
                    uart.write (("/turn/run -50 \r\n").encode())
                elif (off_axis > 70) :
                    print ("turn left8")
                    uart.write (("/turn/run 70 \r\n").encode())
                else :
                    print ("go stright3")
                    uart.write (("/goStraight/run 70 \r\n").encode())
            elif (degrees(tag.y_rotation()) < 350 and degrees(tag.y_rotation()) > 180) :
                if (abs(off_axis) < 15) :
                    print ("turn left4")
                    uart.write (("/turn/run 50 \r\n").encode())
                elif (off_axis < -70) :
                    print ("turn right7")
                    uart.write (("/turn/run -50 \r\n").encode())
                elif (off_axis > 50) :
                    print ("turn left8")
                    uart.write (("/turn/run 50 \r\n").encode())
                else :
                    print ("go stright6")
                    uart.write (("/goStraight/run 70 \r\n").encode())
            else :
                if (off_axis < -15) :
                    print ("turn right7")
                    uart.write (("/turn/run -50 \r\n").encode())
                elif (off_axis > 15) :
                    print ("turn left8")
                    uart.write (("/turn/run 50 \r\n").encode())
                else :
                    if (dist < 20) :
                        # print ("stop10")
                        # uart.write (("/stop/run \n").encode())
                        print("apriltag calibrate success")
                        print("turn right")
                        uart.write(("/turn/run -50 \r\n").encode())
                        time.sleep(1)
                        uart.write(("/stop/run \r\n").encode())
                    else :
                        print ("go stright9")
                        uart.write (("/goStraight/run 70 \r\n").encode())

    if (line):
        count = 0
        img.draw_line(line.line(), color = 127)
        print("line.theta() =  %f " % (line.theta()))
        print("line.rho() =  %f " % (line.rho()))
        if (line.rho() < 0) :
            off_axis = - abs(line.rho()) / math.cos(math.radians(line.theta())) - 80
        else :
            off_axis = abs(line.rho()) / math.cos(math.radians(line.theta())) - 80
        #print (" off-axis = %f" % (off_axis))
        if (abs(off_axis) < 30) :
            print("go straight1")
            uart.write(("/goStraight/run 60 \r\n").encode())
        elif (off_axis > 30) :
            if (line.theta() > 50 and line.theta() < 90) :
                print("go straight2")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(0.5)
                print("turn right2")
                uart.write(("/turn/run -50 \r\n").encode())
            elif (line.theta() < 130 and line.theta() > 90) :
                print("go straight3")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn left3")
                uart.write(("/turn/run 50 \r\n").encode())
            else :
                print("turn left4")
                uart.write(("/turn/run 50 \r\n").encode())
        elif (off_axis < -30) :
            if (line.theta() > 50 and line.theta() < 90) :
                print("go straight5")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(0.5)
                print("turn right5")
                uart.write(("/turn/run -50 \r\n").encode())
            elif (line.theta() < 130 and line.theta() > 90) :
                print("go straight6")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn left6")
                uart.write(("/turn/run 50 \r\n").encode())
            else :
                print("turn right7")
                uart.write(("/turn/run -50 \r\n").encode())

    if ((not find) and (not line)) :
        time.sleep(1.5)
        uart.write (("/stop/run \n").encode())

    print("FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A"))
