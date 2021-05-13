import sklearn
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn import preprocessing

data = pd.read_csv("datasets\\car.data")

#Gives a numpy array for each column, this is turning them into a numerical value (ints)
le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
doors = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))

predict = "class"

x = list(zip(buying, maint, doors, persons, lug_boot, safety))
y = list(cls)

#Modeling and training
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=9)
model.fit(x_train, y_train)

acc = model.score(x_test, y_test)
print("Accuracy: " + str(acc) + "\n")


#See how well it did
names = ["unacc", "acc", "good", "vgood"]
predicted = model.predict(x_test)
#Prints out the predicted grade, followed by the input data (xtest), and then what the actual final grade was (yTest)
for i in range(len(x_test)):
    print("Predicted: ", names[predicted[i]], "  Data: ", x_test[i], "   Actual: ", names[y_test[i]])
    n = model.kneighbors([x_test[i]], 9, True)
    print("N: ", n)
