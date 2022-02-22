My first neural network project!

The task was to predict/classify the objects based on their pixels in rgb

E.g, the model will predict based on the class below:

<code>class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']
  </code>
  
Using 2 fully connected layers of `relu` and `softmax`

And compiling them using the `adam` optimizer, then fitting the data with the images and labels and setting the epoch = 5

Epoch is number of times the model has seen the data

Packages used:
1. tensorflow -- to train the model
2. keras -- train & load data
3. numpy -- calculations
4. matplotlib -- plotting output
