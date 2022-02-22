import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import pickle
from matplotlib import style

data = pd.read_csv("student-mat.csv", sep=";")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences", "health"]]
print(data.head())

predict = "G3"
x = np.array(data.drop([predict], 1)) #Features
y = np.array(data[predict]) #Labels

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)


'''
For the steps below, we are saving the model if the score is better than
any previous iterations

E.g, if acc is 85% in the first version and 88% in the 2nd version,
the better acc is going to be saved as a future model

best = 0
for _ in range(30):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    acc = linear.score(x_test,y_test)
    print(acc)

    if acc > best:
        best = acc
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)
'''
# After saving the model, we can rerun the model with the code afterwards

pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)

print("Coefficient : \n", linear.coef_)
print("Intercept value : \n", linear.intercept_)

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

# Plotting
# Change p value to attributes you want to find
p = "health"
style.use("ggplot")
plt.scatter(data[p], data["G3"])

# Setting labels for axis
plt.xlabel(p)
plt.ylabel("Final Grade")
plt.show()