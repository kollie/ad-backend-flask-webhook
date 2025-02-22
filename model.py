import os
import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split

os.chdir(os.path.dirname(__file__))


data = pd.read_csv("data/Advertising.csv", index_col=0)

X_train, X_test, y_train, y_test = train_test_split(
    data.drop(columns=["sales"]), data["sales"], test_size=0.20, random_state=42
)

model = Lasso(alpha=6000)
model.fit(X_train, y_train)

cross_val_train_MSE = cross_val_score(
    model, X_train, y_train, cv=4, scoring="neg_mean_squared_error"
)
cross_val_train_MAPE = cross_val_score(
    model, X_train, y_train, cv=4, scoring="neg_mean_absolute_percentage_error"
)
mse_cross_val = -np.mean(cross_val_train_MSE)
rmse_cross_val = np.mean([np.sqrt(-mse_fold) for mse_fold in cross_val_train_MSE])
mape_cross_val = -np.mean(cross_val_train_MAPE)
print("Train Mean Sales", y_train.mean())
print("MSE Cross: ", mse_cross_val)
print("RMSE Cross: ", rmse_cross_val)
print("MAPE Cross: ", mape_cross_val)
print("**********")
print("MSE Test: ", mean_squared_error(y_test, model.predict(X_test)))
print("RMSE Test: ", np.sqrt(mean_squared_error(y_test, model.predict(X_test))))
print("MAPE Test: ", mean_absolute_percentage_error(y_test, model.predict(X_test)))


model.fit(data.drop(columns=["sales"]), data["sales"])
pickle.dump(model, open("ad_model.pkl", "wb"))
