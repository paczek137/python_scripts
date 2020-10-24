import datetime
import os
import serial
import time

# ===============================================================
# number of tests to be performed
LOOPS_NUMBER = 1

# port number thought which serial communication takes place
COM_PORT_MODEM = "com4"

# global counter of failures
FAIL_COUNTER = 0

# dir for logs
LOG_DIR = "log"

# log filename
LOG_FILENAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log", os.path.basename(__file__) + ".txt")
print(LOG_FILENAME)

# main serial
serial1 = None


# ===============================================================

def append_to_file(text):
    f = open(LOG_FILENAME, "a")
    f.write(text)
    f.close()
    print(text)


# ===============================================================

def openPort(ser, port):
    global FAIL_COUNTER

    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = 0  # non-block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2  # timeout for write

    try:
        ser.open()
        s = "port: " + str(port) + " opened\n"
        append_to_file(s)
    except Exception as e:
        s = "error in opening serial port: " + str(port) + ": " + str(e) + "\n"
        FAIL_COUNTER = FAIL_COUNTER + 1
        append_to_file(s)


# ======================================================

def at_wait_for_response(ser, resp, timeout=45.0):
    global FAIL_COUNTER
    buffer = ""
    log = ""

    start_time = time.time()
    time_log = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " -> "
    append_to_file(time_log)
    while True:
        if (time.time() - start_time) > timeout:
            if resp is "OK":
                log = "No OK in response!\n"
                break
            elif resp is "SYSSTART":
                # BOOT_UP_FAIL_COUNTER = BOOT_UP_FAIL_COUNTER + 1
                log = "Boot-up failure!"
                break
            else:
                log = "No response for command!"
                break
        line = ser.readline().decode()
        if line:
            buffer = buffer + line
            append_to_file(line)
            if resp in buffer:
                log = " <- Response (len: " + str(len(buffer)) + ") found at: " + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-3] + "\n"
                break
            elif "ERROR" in buffer:
                FAIL_COUNTER = FAIL_COUNTER + 1
                break
            elif "EXIT" in buffer:
                st = time.time()
                while True:
                    exit_text = ser.readline().decode()
                    if exit_text:
                        append_to_file(exit_text)
                    if (time.time() - st) > 3.0:
                        break
                    time.sleep(0.1)
                FAIL_COUNTER = FAIL_COUNTER + 1
                break
    if log:
        append_to_file(log)


# ======================================================

def at_send_command(message, ser, resp="OK", waitForResp=1):
    ser.reset_input_buffer()
    ser.write(message.encode())
    if waitForResp:
        at_wait_for_response(ser, resp)


# ======================================================

def tcp_client_test():
    at_send_command("ati\r", serial1)
    at_send_command("at!=\"showver\"\r", serial1)
    at_send_command("at^sips=all,load\r", serial1)
    at_send_command("at+cmee=2\r", serial1)
    at_send_command("at+cgpiaf=1\r", serial1)
    at_send_command("at^siss?\r", serial1)
    at_send_command("at^sica=1,3\r", serial1)
    time.sleep(5)
    at_send_command("at+cgpaddr\r", serial1)
    at_send_command("at^siso=0\r", serial1)
    time.sleep(2)
    at_send_command("at^sisw=0,10\r", serial1, resp="SISW:")
    at_send_command("qwertyiop", serial1, resp="OK")
    at_send_command("at^sisr=0,100\r", serial1)
    at_send_command("at^sisc=0\r", serial1)


# ======================================================

test = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
test = test + "\n" + os.path.basename(__file__) + "\n"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
open(LOG_FILENAME, 'w').close()
append_to_file(test)
serial1 = serial.Serial()
openPort(serial1, COM_PORT_MODEM)

if FAIL_COUNTER > 0:
    s = "Fail!\n"
    append_to_file(s)
    exit()

num = 0
while num < LOOPS_NUMBER:
    num = num + 1
    s = "====================\n"
    s = s + "Loop " + str(num) + " from " + str(LOOPS_NUMBER) + "\n"
    s = s + "====================\n"
    append_to_file(s)

    tcp_client_test()

    if FAIL_COUNTER > 0:
        s = "Fail!\n"
        append_to_file(s)
        break

if FAIL_COUNTER == 0:
    s = "====================\n"
    s = s + "END OK\n"
    s = s + "====================\n"
    append_to_file(s)

serial1.close()
