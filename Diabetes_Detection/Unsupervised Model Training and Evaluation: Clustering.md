# Unsupervised Model Training and Evaluation: Clustering

## **Steps involved in the Clustering and reasoning:**

1.	Decide portion of dataset used – To use the original set without resampling. 
2.	Build pipeline – StandardScaler() and PCA(n_components = 2): Since K-Means is a distance-based algorithm, this difference of magnitude of different features can create a problem. Standardization is needed to bring all the features to the same magnitude. 
3.	Elbow Method to determine the number of clusters to be formed
4.	Clustering via K-means 
5.	Examining the clusters formed via scatterplot
6.	Mapping with supervised labels

## **Model Performance Evaluation**

### **Optimal n_clusters**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189862623-62c60c45-40b2-4dd6-8744-11f9e6269f72.png" width = 300">
</p>

The above cell indicates that n_clusters = 2 will be an optimal number of clusters for this data.

### **Scatterplot:**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189862672-6ed0d1c3-33da-45fc-a1c7-73a9839dd1b3.png" width = 300">
</p>

The scatterplot shows that roughly one-third of the data is misclassified. As computed, 51505 out of 79159 samples are correctly labeled, achieving an accuracy score of 0.65, confirmed by the classification report.

### **Classification report:**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189862721-0689cb46-ef71-46dd-96c4-5468adaf18d0.png" width = 300">
</p>

For imbalance dataset, Kumar (2014) claims that k-means clustering tends to perform badly as some instances of majority class are portioned into minority class, which makes clusters to have equivalent size. From the classification report above, the recall of majority class, 0 is about 4 times higher than the minority class. Even though the accuracy of 0.65 is high, the model is unable to accurately identify diabetes. 

### **Confusion matrix:**
                                                                                                                               
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189862779-7a124168-2da1-42d3-b12e-daeb165d4338.png" width = 300">
</p>                                                                                                                               

From the confusion matrix, the 22246 of False Negative instances is high, meaning that there are a substantial proportion of patients with diabetes who are predicted to have no diabetes.

### **Adjusted rand score (ARI):**

0.05

The low ARI indicates that similarity between two cluster results is low. The labelling is nearly independent. 

### **Adjusted mutual info score (AMI):**

0.018

The low AMI indicates that the two clustering have a smaller number of clusters, regardless of whether there is more information shared. 


## **Performance of unsupervised models**

• Feature selection can improve the accuracy of clustering considerably. The model yields an accuracy of 0.57 using all features, and 0.57 using selected features via SelectKBest. 

• The number of clusters affects the model accuracy. In our experiment, the accuracy becomes lower when the number of clusters is increased. 

• Despite of being fast and efficient, the result of clustering algorithm is not desirable due to the several reasons: 1) this dataset consists of outliers in several features such as h1_glucose and d1_platelets and clustering cannot handle outliers and noise well, 2) it does not work for the non-linear data set, 3) choosing the centroids randomly cannot give fruitful results.
