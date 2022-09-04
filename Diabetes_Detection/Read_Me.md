The study focused on predicting whether the patient has been diagnosed with a particular type of diabetes, Diabetes 
Mellitus using machine learning models. It is a classification task where 0 (not contracted) and 1 (contracted) are 
assigned to each case. Data pre-processing is performed to handle the missing values by removing unnecessary columns, 
columns with 60% of missing values and highly correlated columns. Categorical encoding is performed using the Label 
Encoder and outliers are examined using boxplot. None of the outliers are removed as these outliers might be the 
indication of extreme health conditions due to the nature of this study. 

Different supervised classification models (Decision Tree Classifier (DTC), Extra Trees Classifier (EDTC), KNeighbors 
Classifier (KNN), Random Forest Classifier (RFC), Gaussian Naïve Bayes (GNB) and Gradient Boosting Classifier (GBC)) and 
unsupervised modes (K-means clustering) are built to compare the performance of their base model and the tuned 
model. The study aims to answer the following questions and the findings have been concluded:

• Feature selection can significantly improve model performance in both supervised and unsupervised models.

• Models tend to be bias towards the majority class in imbalance dataset. Resampling can improve the model  accuracy but not in every case due to many reasons such as the quality of the dataset, reduced specificity in the  trade-off of enhanced sensitivity, better representation of model generalization etc.

• Hyperparameter tuning improves the performance of most of the models except Logistic Regression and Gaussian  Naïve Bayes. In the meantime, GridSearchCV and RandomizedSearchCV yields the same results, but  RandomizedSearchCV takes a shorter training time.

• GNB takes the shortest training time and yields the best performance overall in terms of accuracy and recall. 

• EDTC outperforms the rest of the tree modes, but it compromises on the longer training time of around 1 minute.  Generally, tree-models is more computational expensive compared to other simple classifiers.

• GBC takes the longer time to train but does not improve the performance significantly compared to other models.

• K-means clustering yields a similar result in terms of the accuracy compared to the supervised models. However, it  demonstrates an undesirable recall in the classification report. Also, the low adjusted rand score and adjusted  mutual info score suggest a bad labelling, potentially caused by the nature of k-means clustering of being unable to  work well with outliers and non-linear data set. 
