import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

data = pd.read_csv("datasets\\student-matnew.csv", sep=",")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences", "health", "schoolsup", "famsup", "internet", "romantic", "activities", "freetime", "sex", "age"]]
labels = ["Grade 1", "Grade 2", "Study Time", "Failures", "Absences", "Health", "School Support", "Family Support", "Internet", "Romantic", "Activities", "Free Time", "Sex", "Age"]

predict = "G3"

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

#Testing against 10% of data because if the model had the whole dataset, it would know the answer and couldn't learn
#Order of these variables are important
xTrain, xTest, yTrain, yTest = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

#How to read in pickle file
pickleIn = open("studentmodel.pickle", "rb")
#Load into model
linear = pickle.load(pickleIn)

#This will train the model.  Any time the accuracy is greater then the current best, it will set the best to the accuracy and then save it to the pickle file.
bestScore = 0
for _ in range(100000):
    xTrain, xTest, yTrain, yTest = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    #Fit the data to find a best fit line
    linear = linear_model.LinearRegression()
    linear.fit(xTrain, yTrain)

    #Return accuracy of the model
    acc = linear.score(xTest, yTest)
    #print("Accuracy: " + str(acc))

    if acc > bestScore:
        bestScore = acc
        # Saving the model
        # Better for models that take a long ass time to train or accuraries are very high
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)

print("Best Accuracy: ", bestScore*100, "%\n")

"""
#Prints out the predicted grade, followed by the input data (xtest), and then what the actual final grade was (yTest)
predictions = linear.predict(xTest)
for i in range(len(predictions)):
    print(predictions[i], xTest[i], yTest[i])
"""

for i in range(len(labels)):
    print(labels[i], ": ", linear.coef_[i])

print("\nIntercept: " + str(linear.intercept_))

#Saving the model
#Better for models that take a long ass time to train or accuraries are very high
with open("studentmodel.pickle", "wb") as f:
    pickle.dump(linear, f)

"""
#Plotting it
p = "G1"
style.use("ggplot")
pyplot.scatter(data[p], data[predict])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()
"""