# 00 - Import External Dependencies
import cv2, os
import numpy as np
from keras import Sequential
from keras.src.callbacks import EarlyStopping
from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 00 - Import Internal Dependencies
from CNN_Camera.CNN_preprocessing import CNN_preprocessor, CNN_preprocess_all

# 01 - Loading in the dataset
categories = {'prep_speaker': 0, 'prep_tv': 1, 'prep_lamp': 2}
base_dir = "/Volumes/T7/M7/"

images, labels = [], []

for name, label in categories.items():
    folder_path = os.path.join(base_dir, name)

    for file in os.listdir(folder_path):
        in_path = os.path.join(base_dir, name, file)
        images.append(cv2.imread(in_path))
        labels.append(label)
        print(f"[IMG]: {file}")

images = np.array(images)
labels = np.array(labels)

# 02 - Separating the data_extraction into training - validating - testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)
X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# 03 - Building Architecture
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(130, 170, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(3, activation='softmax'),
])


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_validate, y_validate), callbacks=[early_stopping])

evaluation = model.evaluate(X_test, y_test)
print("Test Accuracy:", evaluation[1])

y_predict = np.argmax(model.predict(X_test), axis=1)
cm = confusion_matrix(y_test, y_predict)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Left', 'Center', 'Right'], )
disp.plot(cmap="Purples")
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('CNN - Training vs. Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


precision = precision_score(y_test, y_predict, average='macro')
recall = recall_score(y_test, y_predict, average='macro')
f1_score = f1_score(y_test, y_predict, average='macro')

print(f"precisions: {precision} - recall: {recall} - f1_score: {f1_score}")
"""
model.save("../Models/CNN_model.h5")
print("Model Saved")
"""

