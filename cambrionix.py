import serial, time

SERIALPORT = '/dev/tty.usbserial-DN001P7U'
BAUDRATE = 115200

serial_con = serial.Serial(SERIALPORT, BAUDRATE)

serial_con.bytesize = serial.EIGHTBITS
serial_con.parity = serial.PARITY_NONE
serial_con.stopbits = serial.STOPBITS_ONE
#ser.timeout = 2
serial_con.xonxoff = False   # Software flow control
serial_con.rtscts = False    # Hardware flow control
serial_con.dsrdtr = False    # Hardware flow control
serial_con.writeTimeout = 0

# Create output buffers
output = []
states = []
old_states = []

while True:
    if serial_con.isOpen():
        try:
            # Flush input buffer, discarding all its contents
            serial_con.flushInput()
            # Flush output buffer, aborting current output
            serial_con.flushOutput()
        
            # Write a command
            serial_con.write('state\r\n')
    
            # Turn into list
            for port in range(0,15):
                output.append(serial_con.readline())
    
            # Find the third element of the each state
            for element in output:
                tmp = element.split()
                states.append(tmp[2])
    
            # If any states are 'R', device rebooted, send 'cls'
            for state in states:
                if state is 'R':
                    print 'device rebooted, clearing output...'
                    serial_con.write('cls\r\n')
                    break
    
            for port in range(len(states)):
                if states[port] is not 'R' and states[port] is not old_states[port]:
                    # There's a difference!
                    print output[port]
    
            # Update old states
            old_states = states
    
        # Actual code is done, clean things up and end program
        except Exception, e:
            print 'error communicating...: ' + str(e)
    
        # Close the serial port whether the except was triggered or not
        finally:
            serial_con.close()
    else:
        print 'cannot open serial port'
