# 00 - Import External Dependencies
import cv2, pygame, pygame.midi
import numpy as np
from keras.src.saving import load_model

# 00 - Importing Internal Dependcies
from CNN_Camera.CNN_preprocessing import CNN_preprocessor
from NN_Ring.NN_preprocessing import create_padding
from visualisation_helper import display_scene

# 01 - Importing the pre-trained Models
CNN_model = load_model('Models/cnn_model.h5')
NN_model = load_model('Models/NN_model.h5')

# 02 - Initialising PyGame and related parameters
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()
going = True

screen_width, screen_height = 1150, 610
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Visualization")

# Device setup
device_id = pygame.midi.get_default_input_id()
print(f"[INFO] Connected device ID: {device_id}")
midi_input = pygame.midi.Input(device_id)

# 03 - Initialising Connections
camera = cv2.VideoCapture(1)

# Variables for capturing and processing data
current_rpy = [0, 0, 0]  # roll, pitch, yaw values
previous_button_state = False
current_button_state = False
current_sequence = []

# Control Variables
SPEAKER_controls = [False, 0, 0.5] # on/off - music number id(0-5) - volume_level(0-1)
TV_controls = [False, 0, 0.5] # on/off - channel number id(0-4) - volume_level(0-1)
LAMP_controls = [False, 0, 1.0] # on/off - color number id(0-4) - brightness(0-1)

# 04 - Main PyGame Loop
while going:
    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            going = False

    if midi_input.poll():
        midi_events = midi_input.read(1024)
        midi_events = pygame.midi.midis2events(midi_events, midi_input.device_id)

        for m_event in midi_events:
            data1, data2 = m_event.data1, m_event.data2
            if m_event.status == 176:  # MIDI CC message
                if 1 <= data1 <= 3:
                    current_rpy[data1 - 1] = data2
                elif data1 == 4:
                    current_button_state = data2 == 127

        if current_button_state:
            if not previous_button_state:
                current_sequence = []
                print("[SEQUENCE STARTED]")

                # CNN_Camera PREDICTIONS -----------------------------
                camera_input = camera.read()[1]
                #CNN_image = CNN_preprocessor(camera_input)

                #TEMPORARY FOR TESTING ONLY
                CNN_image = cv2.imread("/Volumes/T7/M7/prep_speaker/speaker1_frame0.jpg")

                CNN_image = np.array(CNN_image)
                CNN_image = np.expand_dims(CNN_image, axis=0)

                CNN_prediction = CNN_model.predict(CNN_image)
                CNN_predicted_label = np.argmax(CNN_prediction, axis=1)

            current_sequence.append(current_rpy.copy())

        if not current_button_state and previous_button_state:
            padded_sequence = create_padding(current_sequence, 54)

            padded_sequence = np.array(padded_sequence)
            padded_sequence = np.expand_dims(padded_sequence, axis=0)

            NN_prediction = NN_model.predict(padded_sequence)
            NN_predicted_label = np.argmax(NN_prediction, axis=1)

            if CNN_predicted_label == 0:
                if NN_predicted_label == 0:
                    print("SPEAKER - DOWN")
                    SPEAKER_controls[0] = False
                elif NN_predicted_label == 1:
                    print("SPEAKER - LEFT")
                    if 0 < SPEAKER_controls[1]:
                        SPEAKER_controls[1] -=1
                elif NN_predicted_label == 2:
                    print("SPEAKER - RIGHT")
                    if SPEAKER_controls[1] < 5: #6 song to choose from
                        SPEAKER_controls[1] += 1
                elif NN_predicted_label == 3:
                    print("SPEAKER - UP")
                    SPEAKER_controls[0] = True
                elif NN_predicted_label == 4:
                    print("SPEAKER - R-LEFT")
                    if 0 < SPEAKER_controls[2]:
                        SPEAKER_controls[2] -= 0.25
                elif NN_predicted_label == 5:
                    print("SPEAKER - R-RIGHT")
                    if SPEAKER_controls[2] < 1:
                        SPEAKER_controls[2] += 0.25

            elif CNN_predicted_label == 1:
                if NN_predicted_label == 0:
                    print("TV - DOWN")
                    TV_controls[0] = False
                elif NN_predicted_label == 1:
                    print("TV - LEFT")
                    if 0 < TV_controls[1]:
                        TV_controls[1] -= 1
                elif NN_predicted_label == 2:
                    print("TV - RIGHT")
                    if TV_controls[1] < 5:  # 6 movies to choose from
                        TV_controls[1] += 1
                elif NN_predicted_label == 3:
                    print("TV - UP")
                    TV_controls[0] = True
                elif NN_predicted_label == 4:
                    print("TV - R-LEFT")
                    if 0 < TV_controls[2]:
                        TV_controls[2] -= 0.25
                elif NN_predicted_label == 5:
                    print("TV - R-RIGHT")
                    if TV_controls[2] < 1:
                        TV_controls[2] += 0.25

            elif CNN_predicted_label == 2:
                if NN_predicted_label == 0:
                    print("LAMP - DOWN")
                    LAMP_controls[0] = False
                elif NN_predicted_label == 1:
                    print("LAMP - LEFT")
                    if 0 < LAMP_controls[1]:
                        LAMP_controls[1] -= 1
                elif NN_predicted_label == 2:
                    print("LAMP - RIGHT")
                    if LAMP_controls[1] < 5:  # 6 colours to choose from
                        LAMP_controls[1] += 1
                elif NN_predicted_label == 3:
                    print("LAMP - UP")
                    LAMP_controls[0] = True
                elif NN_predicted_label == 4:
                    print("LAMP - R-LEFT")
                    if 0 < LAMP_controls[2]:
                        LAMP_controls[2] -= 0.25
                elif NN_predicted_label == 5:
                    print("LAMP - R-RIGHT")
                    if LAMP_controls[2] < 1:
                        LAMP_controls[2] += 0.25

            print(f"SP:{SPEAKER_controls} TV:{TV_controls} LP:{LAMP_controls}")

        previous_button_state = current_button_state

    screen.fill((0, 0,0))
    display_scene(screen, SPEAKER_controls, TV_controls, LAMP_controls)
    # Updating the display and limiting/setting the frame rate [FPS]
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.midi.quit()
pygame.quit()






