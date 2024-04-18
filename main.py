# 00 - Import External Dependencies
import cv2, pygame
import numpy as np
from keras.src.saving import load_model

# 00 - Importing Internal Dependcies
from CNN_Camera.CNN_preprocessing import CNN_preprocessor

# 01 - Importing the pre-trained Models
CNN_model = load_model('Models/cnn_model.h5')

# 02 - Initialising PyGame and related parameters
pygame.init()
pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()
going = True

# 03 - Initialising Connections
camera = cv2.VideoCapture(1)

# 04 - Main PyGame Loop
while going:
    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            going = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_c:

                # CNN_Camera PREDICTIONS
                camera_input = camera.read()[1]
                CNN_image = CNN_preprocessor(camera_input)

                CNN_image = np.array(CNN_image)
                CNN_image = np.expand_dims(CNN_image, axis=0)

                CNN_prediction = CNN_model.predict(CNN_image)
                CNN_predicted_label = np.argmax(CNN_prediction, axis=1)

                print(CNN_prediction)

                if CNN_predicted_label == 0:
                    print("Label 0 - Speaker")
                elif CNN_predicted_label == 1:
                    print("Label 1 - TV")
                elif CNN_predicted_label == 2:
                    print("Label 2 - Lamp")




    # Updating the display and limiting/setting the frame rate [FPS]
    pygame.display.flip()
    clock.tick(60)







