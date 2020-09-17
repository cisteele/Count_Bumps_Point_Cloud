# Count_Bumps_Point_Cloud

## Challenge

Develop an algorithm by any means (matlab, python, etc) that will automatically detect how many bumps are present in the point cloud.

The bumps_16 file is a test-case where you have a known number of bumps (16 bumps) and can test your algorithm for accuracy. 

The file has one point per line and is comma-delimited (format: X,Y,Z)!

## Files

bumps.txt is the test data.

bumps_16.txt is the training data with a known solution, 16 bumps.

count_bumps_DBSCAN.py is a python file that imports dependencies (numpy, pandas, sklearn) and defines the count_bumps_DBSCAN function.  It can be run in a python IDE of choice (VScode, Spyder).  After running, call the function count_bumps_DBSCAN() with the path to your desired csv dataset and it will return the number of bumps.

count_bumps_DBSCAN_test.py is a python file that defines count_bumps_DBSCAN, and the calls that function with the bumps.txt file as the arguement.  It returns the solution to the number of bumps on the test data. 

Count_Bumps_Point_Cloud_DBSCAN.ipynb is a jupyter notebook with the count_bumps function and an example of it solving the bumps_16.txt and then bumps.txt datasets and timing the solution.  

Count_Bumps_Point_Cloud_EDA.ipynb is a jupyter notebook that shows my exploratory process for loading, cleaning, and visualizing the data before designing the DBSCAN model.  It contains notes of my thought process in markdown cells.  

pastedImagebase640.png is a visual representation of the point cloud in bumps_16.

## Function

This function, count_bumps_DBSCAN, is designed to count the number of structures in a 3D point cloud that rise above (or fall below) the flat 2D plane at height 0.  

The function requires numpy imported as np, pandas imported as pd, and the DBSCAN class imported from sklearn.cluster.

The function first removes all datapoints at height 0, then inputs the lateral coordinates (components 0 and 1) into the Density-Based Spacial Clustering Applications with Noise model, https://en.wikipedia.org/wiki/DBSCAN.  

The DBSCAN model operates by selecting a random point in the dataset, then counts the number of points which are within a distance set by the epsilon value (eps) hyperparameter.  Then, if that count is higher than the min_samples hyperparameter, the model creates a cluster and continues adding any points to that cluster that are within distance episolon of another point in the cluster.  Once there are no more points to add to the cluster, the model picks a random new point and begins the process anew.  Any points that are not within epsilon distance of a number of other points greater than min_samples will be labeled as noise with a -1 and not addeed to any cluster. 

This function does not take advantage of any data about the height of the bumps, and will count bumps of any shape (snaking hills, long walls, donuts, bumps that have bumps on them will be counted as 1).  It will also find dips below height 0 (holes and valleys). 

Please note that this function only works on datasets where the majority of datapoints are part of a flat 2D plane at height 0 and all bumps are spaced at least 6 units from the nearest bump.

## Conclusion

I chose this algorithm because it is a fast and simple way to find raised areas from a 2d array. It does not require the values be quantized to a grid, it does not require the bumps to be round or smooth, and it does not spend resources iterating through the entire dataset mutiple times. Also, it only require common python libraries: numpy, pandas, and sklearn.

I manually discovered the hyperparametes eps = 6 and min_samples = 2 by using knowledge of the use case, dataset, and a few minutes of trial and error. However, for a better tuned model we could use a grid search to find the best hyperparameters. However, in this case with only one training dataset which contains only 16 instances, I do not believe a grid search would be especially effective.

One of the major drawbacks to my approach is the step removing all datapoints with height 0. For point clouds with continuous surfaces and no flat ground state this approach will not work. The bumps must be spaced apart with flat areas between.

The major advantage of my approach is the model will detect bumps of any shape (like donuts).

Other approaches I considered include:

Quantize all datapoints to a grid, then write an algorithm that found all local maxima in the z direction (height) along all slices in the x direction. Then repeated that for all slices in the y direction. Points that were a local maxima in bose cases would also be a 3D local maximum. I believe the findpeaks function in matlab would be effective for this approach. I am concerned that it would be a slow process to iterate through large point clouds.

Finding or writing a 3D array gradient descent algorithm and have it start at random points until it stops finding new local extrema, then count the number of extrema. I know the math behind gradient descent for a function that describes a 3D surface, but I was unsure how to implement that into a point cloud with no continuous function describing the surface. I was also unsure of the best method to deal with cases where it finds the boundary edge instead of a local extrema.

Use some sort of edge detecting library to find the edges of the "targets" created in the 2d heatmap with height as color. This idea ultimately lead me to remembering the DBSCAN clustering algorithm that I had used in the past and so I shifted to that appraoch instead.
