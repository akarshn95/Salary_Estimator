#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

#%%
df = pd.read_csv('glassdoor_data.csv')
df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry','Sector','Revenue','num_comp','hourly','employer_provided',
             'job_state','same_state','age','python_yn','spark','aws','excel','job_simp','seniority','desc_len']]
# %%
df_dummies = pd.get_dummies(df_model)

# %%
X = df_dummies.drop(columns='avg_salary', axis=1)
y = df_dummies['avg_salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# %%
# fit stats model to understand the data better
X_sm = X = sm.add_constant(X)
s_model = sm.OLS(y,X_sm)
s_model.fit().summary()

#%%
lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train,y_train, scoring = 'neg_mean_absolute_error', cv=4))
# %%
ls = Lasso(alpha=0.1)
ls.fit(X_train, y_train)

y_pred = ls.predict(X_test)

#mean_squared_error(y_test, y_pred)
np.mean(cross_val_score(ls, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))
#%%
# tuning for alpha
alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    ls = Lasso(alpha=i/100)
    error.append(np.mean(cross_val_score(ls, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

print(max(error))
plt.plot(alpha,error)

# %%
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

# %%
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

#gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
#gs.fit(X_train,y_train)

#gs.best_score_
#gs.best_estimator_

# %%
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

steps = [('scaler',StandardScaler()),('rf',RandomForestRegressor(criterion='mae', n_estimators=170, max_features='auto'))]
pipeline = Pipeline(steps)

pipeline.fit(X_train,y_train)

print(np.mean(cross_val_score(pipeline, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

#%%
# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_ls = ls.predict(X_test)
tpred_rf = pipeline.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_ls)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)# %%


# %%
