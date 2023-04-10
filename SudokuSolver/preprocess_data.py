import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file, nrows=None):
    data = pd.read_csv(file) if nrows is None else pd.read_csv(file, nrows= nrows)

    features_raw = data['quizzes']
    labels_raw = data['solutions']

    features = []
    labels = []

    for row in features_raw:
        x = np.array([int(i) for i in row]).reshape((9,9,1))
        features.append(x)
    
    features = np.array(features)
    features = features/9
    features -= .5    
    
    for row in labels_raw:
        x = np.array([int(i) for i in row]).reshape((81,1)) - 1
        labels.append(x)   
    
    labels = np.array(labels)
    
    del(features_raw)
    del(labels_raw)  

    print(features)
    print(labels)  

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    
    return x_train, x_test, y_train, y_test

