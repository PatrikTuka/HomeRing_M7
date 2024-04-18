############### -  WAVE SOFTWARE SETUP FOR THE RING - ###############
# A - use standalone mode
# B - Channels [1, 2, 3, 4] = [roll, pitch, yawn, button_momentary]
# C - modify clicks reset - activate, numbers = presets

# ------
# BUTTON COMMANDS
# TOP - on/off
# CENTER - record
# BOTTOM - resets
############################ -  HEADER - ############################
# This code is inspired by the Genki Wave Example: run_midi.py
# Contributors: Anna Kefala, Patrik Tuka

# EVENT-TYPE BASED COLOUR-SCHEME
# [magenta] = Connection Information Event
# [blue] = Keypress Event
# [red] = Data Writing Event
# [yellow] = Sequence Related Event

# For formatting JSON files in PyCharm: Command + Option + L

# 00 - Importing External Dependencies
import pygame, json

# 00 - Import Internal Dependencies
import midi_helper
import colour_lookup as clu

# 01 - Initialising PyGame and related parameters
pygame.init()
pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()
going = True

# 02 - Finding the connected WaveRing ID and device_name
device_id, device_name = midi_helper.get_wave_device_info()
print(f"{clu.magenta}[INFO]:{clu.reset} {device_name} device connected with ID {device_id}.")

# 03 - Defining Input Device
midi_input = pygame.midi.Input(device_id)
print(midi_input)

# 04 - Variables for storing incoming data
current_rpy = [0, 0, 0]
previous_button_state = False
current_button_state = False

# 05 - Variables for saving data
all_recordings = []
current_recording = {}
current_sequence = []
current_label = "NO_LABEL"

# 06 - Our Main Pygame Loop
while going:
    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            going = False
        if event.type == pygame.KEYDOWN:
            # Key events for label allocation [1 2 3 4 5 6]
            if event.key == pygame.K_1:
                current_label = "Move Up"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 1 pressed. Label set to {current_label}")
            if event.key == pygame.K_2:
                current_label = "Move Down"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 2 pressed. Label set to {current_label}")
            if event.key == pygame.K_3:
                current_label = "Move Left"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 3 pressed. Label set to {current_label}")
            if event.key == pygame.K_4:
                current_label = "Move Right"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 4 pressed. Label set to {current_label}")
            if event.key == pygame.K_5:
                current_label = "Rotate Left"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 5 pressed. Label set to {current_label}")
            if event.key == pygame.K_6:
                current_label = "Rotate Right"
                print(f"{clu.blue}[KEY]:{clu.reset} Key 6 pressed. Label set to {current_label}")

            # Key event for saving collected data into a json file [q]
            if event.key == pygame.K_q:
                file_path = "training_data/Patrik-1.json"
                with open(file_path, "w") as json_file:
                    json.dump(all_recordings, json_file)
                print(f"{clu.red}[SAVE]:{clu.reset} Data saved into file: {file_path}")

    # Check if there is any data in the buffer of the midi-device. If not, continue with the loop.
    if not midi_input.poll():
        continue

    # Read all the data from the midi buffer (max_size=1024)
    midi_events = midi_input.read(1024)
    midi_events = pygame.midi.midis2events(midi_events, midi_input.device_id)

    previous_button_state = current_button_state

    # c_m_e = Current Midi Event
    for c_m_e in midi_events:
        if c_m_e.status == 176:
            # [1 - roll] [2 - pitch] [3 - yaw] [4 - button_change]
            if c_m_e.data1 == 1:
                current_rpy[0] = c_m_e.data2
            if c_m_e.data1 == 2:
                current_rpy[1] = c_m_e.data2
            if c_m_e.data1 == 3:
                current_rpy[2] = c_m_e.data2
            if c_m_e.data1 == 4:
                if c_m_e.data2 == 0:
                    current_button_state = False
                elif c_m_e.data2 == 127:
                    current_button_state = True

    # --------------------------------------------

    if current_button_state == True:
        if previous_button_state == False:
            # Create an empty list
            current_sequence = []
            print(f"{clu.yellow}[SEQ]:{clu.reset} Sequence created.")

        # Add the current [RPY] value to current_recordings
        current_sequence.append(current_rpy.copy())
        print(f"Sequence appended: {current_rpy}")

    if current_button_state == False and previous_button_state == True:
        # If it is the end of the sequence we append the recordings to all_recordings with a specific label
        current_recording["label"] = current_label
        current_recording["sequence"] = current_sequence
        all_recordings.append(current_recording.copy())
        print(f"{clu.yellow}[SEQ]:{clu.reset} Data saved into all_recordings with label {current_label}")
        print(current_recording)

    # --------------------------------------------

    # Updating the display and limiting/setting the frame rate [FPS]
    pygame.display.flip()
    clock.tick(60)

del midi_input