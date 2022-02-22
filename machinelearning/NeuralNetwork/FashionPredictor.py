import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist # Loading data

(train_images, train_labels), (test_images, test_labels) = data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# model is going to classify 0 - tshirt, 9-ankle boot etc
# Shrinking values

train_images = train_images/255.0
test_images = test_images/255.0

# Creating a model / Defining architecture
'''
Flatten - input layer flattened so its passable to other neurons
Dense layer 1 - Fully connected layer, "relu" = rectify linear unit
Dense layer 2 - 2nd Dense layer with 10 neurons, "softmax" = pick value for each neuron, add them up to 1
epochs - how many times the model see the data
'''


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
    ])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_images, train_labels, epochs=5)

# Taking highest value and setting it to the predicted value
prediction = model.predict(test_images)

# Looping to show the prediction/ Showing the image in pyplot

for i in range(5):
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel("Actual " + class_names[test_labels[i]])
    plt.title("Prediction " + (class_names[np.argmax(prediction[i])]))
    plt.show()



