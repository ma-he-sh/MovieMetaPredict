import json
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import os
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


def get_dataset_list():
    file_list = []
    dataset_dir = os.path.abspath(__file__ + "/../../../")
    for file in os.listdir(dataset_dir + "/dataset/dataset_cleaned"):
        if file.endswith(".json"):
            file_list.append(os.path.join(dataset_dir + "/dataset/dataset_cleaned", file))
    return file_list


def knn():
    # # loading data
    file_list = get_dataset_list()
    dataframes = []
    for file in file_list:
        with open(file) as data_file:
            data = json.load(data_file)
        json_d = pd.json_normalize(data)
        dataframes.append(json_d)
    df = pd.concat(dataframes)

    # col = ['fear', 'joy', 'negative', 'sadness', 'surprise', 'positive', 'trust', 'anticipation', 'anger', 'disgust',
    #        'rating']
    col = ['negative','rating']
    df = df[col].replace(np.NAN,0)
    X = df.iloc[:, :-1].values
    Y = df.iloc[:, 1].values

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)

    # for r in X_train:
    #     print(r)
    #
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    classifier = KNeighborsClassifier(n_neighbors=8)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    result = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(result)
    result1 = classification_report(y_test, y_pred, zero_division=1)
    print("Classification Report:", )
    print(result1)
    result2 = accuracy_score(y_test, y_pred)
    print("Accuracy:", result2)


knn()
