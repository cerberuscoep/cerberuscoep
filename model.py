import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import pickle

housing = pd.read_csv("housing.csv")
train_set, test_set = train_test_split(housing, test_size = 0.2, random_state = 42)
split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)
for train_index, test_index in split.split(housing, housing["CHAS"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

housing = strat_train_set.copy()
#skiping correlation matrix here


#spliting training and testing set

housing = strat_train_set.drop("MEDV", axis=1)
housing_labels = strat_train_set["MEDV"].copy()

my_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")), 
    ('std_scaler', StandardScaler())
])

housing_num_tr = my_pipeline.fit_transform(housing) #returns numpy array
model = LinearRegression()
model.fit(housing_num_tr, housing_labels)

# from joblib import dump, load
# dump(model, "Dragon.joblib")

pickle_out = open("dict.pickle","wb")
pickle.dump(model, pickle_out)
pickle_out.close()


# X_TEST = [[int(input()), int(input()), int(input())]]
# outcome = predictor.predict(X=X_TEST)
# coefficients = predictor.coef_

# print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))    
