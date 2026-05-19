import serial
import time

PORT = str(input('PORT: ')) #"/dev/ttyUSB1"
BAUD_RATE = int(input('BAUD RATE: ')) # 1_000_000

STARTUP_MESSAGE = "RR_SHIELD_READY"
DONE_MESSAGE = "DONE"

def cmdList():
    cmds = '''
    // '0' — testShield: chip ID verification
    // '1' — REMOVED
    // '2' — REMOVED
    // '3' — REMOVED
    // '4' — Test 1: REMOVED
    // '5' — Test 2: REMOVED
    // '6' — Test 3: REMOVED
    // '8' — Test 5: comparator bit extraction, all banks, all 8 enroll
    levels
    // 'b' — Test 8: cross comparator sweep, P×P addresses, all 4 banks;
    level and step sent as next 2 bytes
    // 'e' — Test 11a: REMOVED
    // 'f' — Test 11b: REMOVED
    // 'g' — Test 12: comparator sweep all 4096 addresses, level index sent
    as next byte
    \n
    '''
    print(cmds)
    return None

def wait_for_startup(ser):
    """
    Wait until the exact startup message appears once.
    Safe even if it arrives immediately after reset.
    """
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            print(f"RR_SHIELD: {line}")

            if line == STARTUP_MESSAGE:
                return


def wait_for_done(ser):
    """
    Wait until DONE is received.
    """
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            print(f"RR_SHIELD: {line}")

            if line == DONE_MESSAGE:
                return


def main():
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=0.2) # Connect to port 
        time.sleep(2)  # Allow reset after opening port
        print(f"Connected to {PORT}")
        print(f"Waiting for startup message: {STARTUP_MESSAGE}")
        wait_for_startup(ser)
        # print("Board is ready.\n")

        while True: # Interation loop
            cmd = input("Enter command (q to quit): ")
            
            if cmd.lower() == "h": # Open help menu 
                cmdList()
                continue
            
            if cmd.lower() == "q": # Go to close serial connection 
                break

            ser.write((cmd).encode())

            print(f"Waiting for '{DONE_MESSAGE}'...")
            wait_for_done(ser)

            print("Done.\n")

        ser.close() # Once the loop is broken (using q) close the connection

    except serial.SerialException as e:
        print(f"Serial error: {e}")


if __name__ == "__main__":
    main()