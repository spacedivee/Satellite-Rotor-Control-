import time
import board
import busio
import digitalio
import rotaryio
import displayio
import terminalio
import usb_cdc
from adafruit_display_text import label
import adafruit_ssd1306

# --- 1. Initialize Status LED (Pin 14 / D11) ---
status_led = digitalio.DigitalInOut(board.D11)
status_led.direction = digitalio.Direction.OUTPUT
status_led.value = False

def flash_led():
    """Blinks the status LED quickly when a command is sent."""
    status_led.value = True
    time.sleep(0.05)
    status_led.value = False

# --- 2. Initialize 128x32 OLED Display (SDA=D9, SCL=D10) ---
displayio.release_displays()
i2c = busio.I2C(scl=board.D10, sda=board.D9)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_ssd1306.SSD1306(display_bus, width=128, height=32)

# --- 3. Easy UI Formatting ---
splash = displayio.Group()
display.root_group = splash

title_text = label.Label(terminalio.FONT, text="TRACKER ACTIVE", x=2, y=6)
az_text = label.Label(terminalio.FONT, text="AZ: 180°", x=2, y=22)
el_text = label.Label(terminalio.FONT, text="EL: 00°", x=70, y=22)

splash.append(title_text)
splash.append(az_text)
splash.append(el_text)

def update_screen(az_val, el_val):
    az_text.text = f"AZ: {az_val:03d}°"
    el_text.text = f"EL: {el_val:02d}°"

# --- 4. Initialize 2x2 Button Matrix ---
# Rows (Outputs)
row_pins = [board.D0, board.D1]
rows = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row in rows:
    row.direction = digitalio.Direction.OUTPUT
    row.value = True  # High by default

# Columns (Inputs)
col_pins = [board.D2, board.D3]
cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col in cols:
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP  # Pull-up required due to ground-facing matrix diodes

# Matrix state tracking memory to avoid repeated spamming
# Matrix map index: [0]=Azimuth+1, [1]=Elevation+1, [2]=Azimuth-1, [3]=Elevation-1
button_states = [True] * 4 

# --- 5. Initialize Rotary Encoder & Switch (A=D4, B=D5, SW=D6) ---
encoder = rotaryio.IncrementalEncoder(board.D4, board.D5)
last_encoder_position = encoder.position

enc_switch = digitalio.DigitalInOut(board.D6)
enc_switch.direction = digitalio.Direction.INPUT
enc_switch.pull = digitalio.Pull.UP
last_switch_state = True

# Live Variables
target_az = 180 
target_el = 0
control_mode = "AZ"  # Knob controls Azimuth first. Click to switch to Elevation.

def send_command(cmd_string):
    usb_cdc.console.write(f"{cmd_string}\n".encode('utf-8'))
    flash_led()

# Set starting baseline text
update_screen(target_az, target_el)

# --- 6. Main Control Loop ---
while True:
    # --- Matrix Scanning Routine ---
    current_matrix_clicks = [True] * 4
    
    # Scan Row 0 (Azimuth +1 and Elevation +1)
    rows[0].value = False  # Pull Row 0 Low
    current_matrix_clicks[0] = cols[0].value  # Read Col 0 (Azimuth +1)
    current_matrix_clicks[1] = cols[1].value  # Read Col 1 (Elevation +1)
    rows[0].value = True   # Reset Row 0 High

    # Scan Row 1 (Azimuth -1 and Elevation -1)
    rows[1].value = False  # Pull Row 1 Low
    current_matrix_clicks[2] = cols[0].value  # Read Col 0 (Azimuth -1)
    current_matrix_clicks[3] = cols[1].value  # Read Col 1 (Elevation -1)
    rows[1].value = True   # Reset Row 1 High

    # Process Matrix Click Actions (Trigger on Press Down / Fall to False)
    if not current_matrix_clicks[0] and button_states[0]:  # Azimuth +1 Button
        target_az = (target_az + 1) % 360
        send_command(f"GOTO AZ={target_az} EL={target_el}")
        update_screen(target_az, target_el)
        
    elif not current_matrix_clicks[2] and button_states[2]:  # Azimuth -1 Button
        target_az = (target_az - 1) % 360
        send_command(f"GOTO AZ={target_az} EL={target_el}")
        update_screen(target_az, target_el)
        
    elif not current_matrix_clicks[1] and button_states[1]:  # Elevation +1 Button
        target_el = max(0, min(90, target_el + 1))
        send_command(f"GOTO AZ={target_az} EL={target_el}")
        update_screen(target_az, target_el)
        
    elif not current_matrix_clicks[3] and button_states[3]:  # Elevation -1 Button
        target_el = max(0, min(90, target_el - 1))
        send_command(f"GOTO AZ={target_az} EL={target_el}")
        update_screen(target_az, target_el)

    # Save current matrix scan state for next loop iteration
    button_states = current_matrix_clicks

    # --- Rotary Encoder Scanning ---
    current_encoder_position = encoder.position
    if current_encoder_position != last_encoder_position:
        direction = 1 if current_encoder_position > last_encoder_position else -1
        
        # Dial Fine Tuning
        if control_mode == "AZ":
            target_az = (target_az + direction) % 360
        elif control_mode == "EL":
            target_el = max(0, min(90, target_el + direction))
        
        send_command(f"GOTO AZ={target_az} EL={target_el}")
        update_screen(target_az, target_el)
        last_encoder_position = current_encoder_position

    # --- Encoder Knob Click Toggle (Toggles Knob Focus) ---
    if not enc_switch.value and last_switch_state:
        if control_mode == "AZ":
            control_mode = "EL"
            title_text.text = "TUNE MODE: ELEV"
        else:
            control_mode = "AZ"
            title_text.text = "TUNE MODE: AZIM"
        time.sleep(0.15)  # Debounce delay
    last_switch_state = enc_switch.value

    time.sleep(0.01)  # General loop pacing
