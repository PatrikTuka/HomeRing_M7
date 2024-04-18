# 00 - Import External Dependencies
import numpy as np

from keras import Sequential, Input
from keras.src.layers import Flatten, Dense, Dropout

from matplotlib import pyplot as plt

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
import seaborn as sns

# 00 - Import Internal Dependencies
from NN_Ring.NN_preprocessing import NN_preprocessor

# 01 - Importing and splitting data
data, max_length = NN_preprocessor('training_data')

labels, sequences = [], []
for entry in data:
    labels.append(entry["label"])
    sequences.append(entry["sequence"])

encoder = LabelEncoder()
encoded_labels = encoder.fit_transform(labels)
encoded_labels = tf.keras.utils.to_categorical(encoded_labels)

encoded_labels = np.array(encoded_labels)
sequences = np.array(sequences)

# 02 - Separating the data_extraction into training - validating - testing sets
X_train, X_test, y_train, y_test = train_test_split(sequences, encoded_labels, test_size=0.2, random_state=42)
X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# 03 - Building Architecture
model = Sequential([
    Input(shape=(max_length, 3)),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax'),
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=300, batch_size=64, validation_data=(X_validate, y_validate))


model.summary()
evaluation = model.evaluate(X_test, y_test)
print("Test Accuracy:", evaluation[1])

y_predict = np.argmax(model.predict(X_test), axis=1)

y_test_decoded = []

for x in range(len(y_test)):
    y_test_decoded.append(np.argmax(y_test[x]))

y_test_decoded = np.array(y_test_decoded)


# Compute and plot confusion matrix
cm = confusion_matrix(y_test_decoded, y_predict)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

model.save("../Models/NN_model.h5")


