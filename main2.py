# 00 - Import External Dependencies
import pygame
import pygame.midi
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# 00 - Import Internal Dependencies
from NN_Ring.NN_preprocessing import create_padding

# Initialize Pygame and the MIDI input
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()
going = True

# Display setup
pygame.display.set_mode((100, 100))

# Load the LSTM model and StandardScaler
NN_model = load_model('Models/NN_model.h5')

# Device setup
device_id = pygame.midi.get_default_input_id()
print(f"[INFO] Connected device ID: {device_id}")
midi_input = pygame.midi.Input(device_id)

# Variables for capturing and processing data
current_rpy = [0, 0, 0]  # roll, pitch, yaw values
previous_button_state = False
current_button_state = False
current_sequence = []

# Main event loop
while going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
            current_sequence.append(current_rpy.copy())


        if not current_button_state and previous_button_state:
            padded_sequence = create_padding(current_sequence, 66)

            padded_sequence = np.array(padded_sequence)
            padded_sequence = np.expand_dims(padded_sequence, axis=0)

            prediction = NN_model.predict(padded_sequence)
            predicted_label = np.argmax(prediction, axis=1)

            print(f"Predicted Label: {prediction}")
            if predicted_label == 0:
                print("DOWN") # UP
            elif predicted_label == 1:
                print("LEFT") # DOWN
            elif predicted_label == 2:
                print("LEFT") # LEFT???
            elif predicted_label == 3:
                print("UP") # RIGHT
            elif predicted_label == 4:
                print("R-LEFT") # R-LEFT
            elif predicted_label == 5:
                print("R-RIGHT") # R-RIGHT

        previous_button_state = current_button_state

    pygame.display.flip()
    clock.tick(60)

