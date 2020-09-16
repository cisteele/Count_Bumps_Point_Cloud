#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

def count_bumps_DBSCAN(point_cloud_csv_path):
    # These hyperparameters could easily be added as arguements to the definition above
    eps = 6
    min_samples = 2
    
    # Create a DataFrame with 3 fields: 0, 1, and 2 (corresponding to x, y, and z).
    df = pd.read_csv(point_cloud_csv_path, header = None)
    
    # Remove all datapoints with component 2 having a value of 0.
    df_bumps = df[df[2] != 0]
    
    # Define Density Based Spacial Clustering Applications w/ Noise clustering model.
    # The hyperparameters for this model were manually discovered using the bumps_16.txt training data.
    dbscan_cluster = DBSCAN(eps=eps, min_samples=min_samples)
    
    # Fit model and create an array with the cluster label for each datapoint
    clusters = dbscan_cluster.fit_predict(df_bumps[[0, 1]])
    
    # Count the number of unique cluster labels.
    bump_count = np.unique(clusters)
    
    # Return that value as the number of bumps.
    return len(bump_count)

print(count_bumps_DBSCAN('bumps.txt'))

