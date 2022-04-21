#!/usr/bin/env python


from sklearn.model_selection import RandomizedSearchCV
import hdbscan
from sklearn.metrics import make_scorer
import numpy as np

import pandas as pd

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

SEED = 42
np.random.seed(SEED)  # set the random seed as best we can

df = pd.read_csv('BaynesSoundMooring_40mbss_ConductivityTemperatureDepth_20200305T000000Z_20200313T210509Z-NaN.csv',skipinitialspace=True)
df.rename(columns={df.columns[0]: 'UTC time', df.columns[1]: 'Conductivity',df.columns[15]: 'Temperature'},inplace=True)
X = df[['Conductivity','Temperature']].values

# Standardize data
scaler = StandardScaler() 
scaled_df = scaler.fit_transform(X) 
  
X_principal = pd.DataFrame(scaled_df) 

hdb = hdbscan.HDBSCAN(gen_min_span_tree=True).fit(X_principal)

# specify parameters and distributions to sample from
param_dist = {#'min_samples': [20,40,60,80,100,120,140,160,180,200],
              'min_samples':20,
            # 'min_cluster_size':[50,100,150,200,250,300,350], 
              'min_cluster_size':200, 
              'cluster_selection_epsilon': 0.1,
              'cluster_selection_method' : ['eom','leaf'],
              'metric' : ['euclidean','manhattan'] 
             }

#validity_scroer = "hdbscan__hdbscan___HDBSCAN__validity_index"
validity_scorer = make_scorer(hdbscan.validity.validity_index,greater_is_better=True)


n_iter_search = 20
random_search = RandomizedSearchCV(hdb
                                   ,param_distributions=param_dist
                                   ,n_iter=n_iter_search
                                   ,scoring=validity_scorer 
                                   ,random_state=SEED)

random_search.fit(X_principal)


print(f"Best Parameters {random_search.best_params_}")
print(f"DBCV score :{random_search.best_estimator_.relative_validity_}")
