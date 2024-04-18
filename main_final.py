# 00 - Import External Dependencies
import cv2, pygame, pygame.midi
import numpy as np
from keras.src.saving import load_model

# 00 - Importing Internal Dependcies
from CNN_Camera.CNN_preprocessing import CNN_preprocessor
from NN_Ring.NN_preprocessing import create_padding

# 01 - Importing the pre-trained Models
CNN_model = load_model('Models/cnn_model.h5')
NN_model = load_model('Models/NN_model.h5')

# 02 - Initialising PyGame and related parameters
pygame.init()
pygame.midi.init()
pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()
going = True

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
                CNN_image = CNN_preprocessor(camera_input)

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
                    print("SPEAKER - DOWN")  # UP
                elif NN_predicted_label == 1:
                    print("SPEAKER - LEFT")  # DOWN
                elif NN_predicted_label == 2:
                    print("SPEAKER - RIGHT")  # LEFT???
                elif NN_predicted_label == 3:
                    print("SPEAKER - UP")  # RIGHT
                elif NN_predicted_label == 4:
                    print("SPEAKER - R-LEFT")  # R-LEFT
                elif NN_predicted_label == 5:
                    print("SPEAKER - R-RIGHT")  # R-RIGHT

            elif CNN_predicted_label == 1:
                if NN_predicted_label == 0:
                    print("TV - DOWN")  # UP
                elif NN_predicted_label == 1:
                    print("TV - LEFT")  # DOWN
                elif NN_predicted_label == 2:
                    print("TV - RIGHT")  # LEFT???
                elif NN_predicted_label == 3:
                    print("TV - UP")  # RIGHT
                elif NN_predicted_label == 4:
                    print("TV - R-LEFT")  # R-LEFT
                elif NN_predicted_label == 5:
                    print("TV - R-RIGHT")  # R-RIGHT

            elif CNN_predicted_label == 2:
                if NN_predicted_label == 0:
                    print("LAMP - DOWN")  # UP
                elif NN_predicted_label == 1:
                    print("LAMP - LEFT")  # DOWN
                elif NN_predicted_label == 2:
                    print("LAMP - RIGHT")  # LEFT???
                elif NN_predicted_label == 3:
                    print("LAMP - UP")  # RIGHT
                elif NN_predicted_label == 4:
                    print("LAMP - R-LEFT")  # R-LEFT
                elif NN_predicted_label == 5:
                    print("LAMP - R-RIGHT")  # R-RIGHT






        previous_button_state = current_button_state


    # Updating the display and limiting/setting the frame rate [FPS]
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.midi.quit()
pygame.quit()






